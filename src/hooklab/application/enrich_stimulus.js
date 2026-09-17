export async function enrichStimulus({ stimulus, cognitivePort }) {
  const descriptors=await cognitivePort.describe(stimulus);
  return Object.freeze({...stimulus,cognitiveDescriptors:Object.freeze([...descriptors])});
}
