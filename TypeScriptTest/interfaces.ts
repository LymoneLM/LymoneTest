// readonly 关键词定义只读属性
// ?可以定义可选属性
interface Person {
    name: string;
    readonly id: number;
    age?: number;
}

const person: Person = {
    name: 'Gabriel',
    id: 123
};

// // 不能指定为Person接口
// const person2: Person = {
//     names: 'Gabriel',
// };

// person.id = 200; // 不可为id赋值因为它是只读的