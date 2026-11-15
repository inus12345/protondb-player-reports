import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { makeCsv, makeXlsx } from './exports.mjs';
const fields=['steamAppId','noteText','databaseLicense'];
const rows=[{steamAppId:'1234567890123456789',noteText:'Works with 🕹️ and 👍; quote " & < >\nSecond line.\r\nWindows newline.',databaseLicense:'https://opendatacommons.org/licenses/odbl/1-0/'},{steamAppId:'42',noteText:'=This stays player text, not a formula',databaseLicense:null}];
function consume(code,bytes){const r=spawnSync('python3',['-c',code],{input:bytes});assert.equal(r.status,0,r.stderr.toString());return JSON.parse(r.stdout.toString());}
test('CSV round-trips full Unicode, quoted multiline notes and string IDs with a standard parser',()=>{
 const b=makeCsv(rows,fields);assert.equal(b.subarray(0,3).toString('hex'),'efbbbf');
 const out=consume("import sys,csv,io,json; print(json.dumps(list(csv.DictReader(io.StringIO(sys.stdin.buffer.read().decode('utf-8-sig'))))))",b);
 assert.equal(out[0].noteText,rows[0].noteText);assert.equal(out[0].steamAppId,rows[0].steamAppId);assert.equal(out[1].databaseLicense,'');
});
test('Excel ZIP/XML preserves non-BMP Unicode and text IDs without formulas, with filters and frozen header',()=>{
 const out=consume("import sys,zipfile,io,xml.etree.ElementTree as E,json; z=zipfile.ZipFile(io.BytesIO(sys.stdin.buffer.read())); assert z.testzip() is None; s=E.fromstring(z.read('xl/worksheets/sheet1.xml')); ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}; assert s.find('.//s:pane',ns).attrib['state']=='frozen'; assert s.find('s:autoFilter',ns) is not None; assert s.find('.//s:f',ns) is None; print(json.dumps([[(''.join(c.find('s:is',ns).itertext())) for c in r.findall('s:c',ns)] for r in s.findall('s:sheetData/s:row',ns)]))",makeXlsx(rows,fields));
 assert.deepEqual(out[0],fields);assert.equal(out[1][0],rows[0].steamAppId);assert.equal(out[1][1],rows[0].noteText);assert.equal(out[2][1],rows[1].noteText);
});
