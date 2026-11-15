import fs from 'node:fs';
import { crc32, deflateRawSync } from 'node:zlib';
const schema=JSON.parse(fs.readFileSync(new URL('./.actor/dataset_schema.json',import.meta.url),'utf8'));
export const exportFields=schema.views.reports.transformation.fields;
const value=(row,key)=>row[key]==null?'':typeof row[key]==='object'?JSON.stringify(row[key]):String(row[key]);
export function makeCsv(rows,fields=exportFields){
 const quoted=s=>'"'+s.replaceAll('"','""')+'"';
 return Buffer.from('\uFEFF'+[fields,...rows.map(r=>fields.map(k=>value(r,k)))].map(row=>row.map(quoted).join(',')).join('\r\n')+'\r\n','utf8');
}
// Store strings directly in OOXML; native dataset XLSX export can strip non-BMP Unicode.
const xml=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&apos;');
const text=s=>xml(s.replace(/_x[0-9a-fA-F]{4}_/g,m=>'_x005F_'+m.slice(1)).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\uFFFE\uFFFF]/g,c=>'_x'+c.charCodeAt(0).toString(16).toUpperCase().padStart(4,'0')+'_')).replaceAll('\r','&#13;');
const col=i=>{let n=i+1,s='';while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26);}return s;};
function zip(files){
 const blocks=[],central=[];let offset=0;
 for(const [path,content] of Object.entries(files)){
  const name=Buffer.from(path),raw=Buffer.from(content),body=deflateRawSync(raw),crc=crc32(raw),h=Buffer.alloc(30),c=Buffer.alloc(46);
  h.writeUInt32LE(0x04034b50);h.writeUInt16LE(20,4);h.writeUInt16LE(0x800,6);h.writeUInt16LE(8,8);h.writeUInt16LE(0x21,12);h.writeUInt32LE(crc,14);h.writeUInt32LE(body.length,18);h.writeUInt32LE(raw.length,22);h.writeUInt16LE(name.length,26);
  c.writeUInt32LE(0x02014b50);c.writeUInt16LE(20,4);c.writeUInt16LE(20,6);c.writeUInt16LE(0x800,8);c.writeUInt16LE(8,10);c.writeUInt16LE(0x21,14);c.writeUInt32LE(crc,16);c.writeUInt32LE(body.length,20);c.writeUInt32LE(raw.length,24);c.writeUInt16LE(name.length,28);c.writeUInt32LE(offset,42);
  blocks.push(h,name,body);central.push(c,name);offset+=h.length+name.length+body.length;
 }
 const directory=Buffer.concat(central),end=Buffer.alloc(22),count=Object.keys(files).length;end.writeUInt32LE(0x06054b50);end.writeUInt16LE(count,8);end.writeUInt16LE(count,10);end.writeUInt32LE(directory.length,12);end.writeUInt32LE(offset,16);return Buffer.concat([...blocks,directory,end]);
}
export function makeXlsx(rows,fields=exportFields){
 const ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main',rel='http://schemas.openxmlformats.org/officeDocument/2006/relationships';
 const data=[fields,...rows.map(r=>fields.map(k=>value(r,k)))];
 const sheet=data.map((row,r)=>`<row r="${r+1}">${row.map((s,c)=>`<c r="${col(c)}${r+1}" t="inlineStr" s="${r===0?1:fields[c]==='noteText'?2:0}"><is><t xml:space="preserve">${text(s)}</t></is></c>`).join('')}</row>`).join('');
 const columns=fields.map((f,i)=>`<col min="${i+1}" max="${i+1}" width="${f==='noteText'?80:f==='gameTitle'?30:26}" customWidth="1"/>`).join('');
 return zip({
  '[Content_Types].xml':'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>',
  '_rels/.rels':`<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="${rel}/officeDocument" Target="xl/workbook.xml"/></Relationships>`,
  'xl/workbook.xml':`<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="${ns}" xmlns:r="${rel}"><sheets><sheet name="Player reports" sheetId="1" r:id="rId1"/></sheets></workbook>`,
  'xl/_rels/workbook.xml.rels':`<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="${rel}/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="${rel}/styles" Target="styles.xml"/></Relationships>`,
  'xl/styles.xml':`<?xml version="1.0" encoding="UTF-8"?><styleSheet xmlns="${ns}"><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts><fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>`,
  'xl/worksheets/sheet1.xml':`<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="${ns}"><dimension ref="A1:${col(fields.length-1)}${data.length}"/><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><sheetFormatPr defaultRowHeight="15"/><cols>${columns}</cols><sheetData>${sheet}</sheetData><autoFilter ref="A1:${col(fields.length-1)}${data.length}"/></worksheet>`
 });
}
