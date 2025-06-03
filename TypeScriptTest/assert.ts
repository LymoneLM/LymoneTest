let str: any = 'I am a String';
// 两种断言指定泛型类型为具体类型，调用对应方法
let strLength = (str as string).length;
let strLength2 = <string>str.length;
console.log(`length of str is ${strLength} or ${strLength2}`);
