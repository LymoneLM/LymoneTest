// 可以定义参数和返回类型
function add(num1: number, num2: number): number {
    return num1 + num2;
}
// 报错
// add(2, '5')
add(2, 5);


// ?可以标记可选参数
function printName(firstName: string, lastName?: string) {
    if (lastName) console.log(`Firstname: ${firstName}, Lastname: ${lastName}`);
    else console.log(`Firstname: ${firstName}`);
}
printName('Gabriel');


// 参数设置默认值
function printName_(firstName: string, lastName: string = 'Tanner') {
    console.log(`Firstname: ${firstName}, Lastname: ${lastName}`);
}
printName_('Gabriel');