const app = new Vue({
    el: '#todoapp',
    delimiters: ['[[', ']]'],
    data: {
        // -- 使用するデータを書く
        // ToDoリストデータ用のカラ配列をdataオプションに登録する。
        todos: [],
        message: "Hello V-on!",
        count_number: 1
    },
    methods: {
        // -- 使用するメソッド
        // ToDo 追加の処理
        doAdd: function (event, value) {
            // ref で名前を付けておいた要素を参照
            var comment = this.$refs.comment
            // 入力がなければ何もしないで return
            if (!comment.value.length) {
                return
            }
            // { 新しいID, コメント, 作業状態 }
            // というオブジェクトを現在の todos リストへ push
            this.todos.push({
                id: uid++,
                comment: comment.value
            })
            // フォーム要素を空にする
            comment.value = ''
        },
        click_count_up: function () {
            this.count_number++;
        }
    }
})