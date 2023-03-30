import drs from "deterministic-random-sequence";
export const colour = function(uid) {
    let index = 0
    let rand = drs("hello")
    for (let i = 0; i < uid + 1; i++) {
        index = Math.round(rand() * 1000)
    }

    return ['red', 'blue', 'green', 'purple', 'pink', 'orange',
        'deep-orange', 'indigo', 'deep-purple', 'amber'][index % 10]
}
