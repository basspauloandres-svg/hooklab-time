const FORBIDDEN_KEYS=new Set(['name','email','phone','address','ip','ipAddress','deviceFingerprint']);
export function assertDataMinimization(value,path='root'){
 if(value&&typeof value==='object') for(const [key,v] of Object.entries(value)){ if(FORBIDDEN_KEYS.has(key)) throw new Error(`forbidden direct identifier at ${path}.${key}`); assertDataMinimization(v,`${path}.${key}`); }
 return true;
}
