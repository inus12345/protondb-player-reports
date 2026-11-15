export function unbilledCount(chargedPrefix, start, count) {
 for(const n of [chargedPrefix,start,count])if(!Number.isSafeInteger(n)||n<0)throw new Error('Invalid native billing count');
 return Math.max(0,start+count-chargedPrefix);
}
