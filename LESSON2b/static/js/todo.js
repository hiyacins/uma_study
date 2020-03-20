const app = new Vue({
    el: '#todoapp',
    delimiters: ['[[', ']]'],
    data: {
        // -- 使用するデータを書く
        // ToDoリストデータ用のカラ配列をdataオプションに登録する。
        todos: [],
        // ToDoリストのid初期化
        id: 1
    },
    methods: {
        // -- 使用するメソッドはここへ
        // ToDoリスト追加の処理
        doAdd: function (event, value) {
            // ref で名前を付けておいた要素を参照
            var comment = this.$refs.comment
            // 入力がなければ何もしないで return
            if (!comment.value.length) {
                return
            }
            // todos リストへ pushする。
            // 例：{ 新しいID, コメント }
            this.todos.push({
                id: this.id++,
                comment: comment.value
            })
            // フォーム要素を空にする
            comment.value = ''
        },
        // ToDoリスト削除の処理
        doRemove: function (item) {
            var index = this.todos.indexOf(item)
            this.todos.splice(index, 1)
        }
    }
})