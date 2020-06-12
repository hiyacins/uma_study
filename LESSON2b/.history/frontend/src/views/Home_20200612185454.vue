<template>
  <div id="todoapp">
    <!--ここにテンプレートを書く-->
    <table>
      <!-- テーブルヘッダー -->
      <thead>
        <tr>
          <th class="id">ID</th>
          <th class="comment">コメント</th>
          <th class="button">-</th>
        </tr>
      </thead>
      <tbody>
        <!-- ここに<tr>でToDoの要素を1行ずつ繰り返し表示したい-->
        <tr v-for="entry in entries" v-bind:key="entry.id">
          <!-- 要素の情報 -->
          <th>{{ entry.id }}</th>
          <td>{{ entry.comment }}</td>
          <td class="button">
            <!-- 削除ボタン -->
            <button v-on:click="doRemove(entry.id)">削除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <h2>新しい作業の追加</h2>
    <form class="add-form" v-on:submit.prevent="doAdd">
      <!-- コメント入力フォーム -->
      コメント
      <input v-model="comment" type="text" name="comment" ref="comment" />
      <!-- 追加ボタン -->
      <button type="submit">追加</button>
    </form>
    <br />
    <form class="add-form">
      <!-- 削除ボタン -->
      <button v-on:click="doAllRemove(entries)">すべて削除</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "todoapp",
  data() {
    return {
      // -- 使用するデータを書く
      // ToDoリストデータ用のカラ配列をdataオプションに登録する。
      entries: [],
      baseUrl: "http://127.0.0.1:5000/"
      // ToDoリストのid初期化
      // id: 241,
    };
  },
  created() {
    axios.get(this.baseUrl + "getjson").then(res => {
      this.entries = res.data;
      console.log(res.data);
    });
  },
  methods: {
    // -- 使用するメソッドはここへ
    async getTodo() {
      try {
        let response = await axios.get(this.baseUrl + "todo");
        this.todoList = response.data;
      } catch (e) {
        console.log(e);
      }
    },
    // ToDoリスト追加の処理
    doAdd(event, value) {
      // ref で名前を付けておいた要素を参照
      var comment = this.$refs.comment;
      // 入力がなければ何もしないで return
      if (!comment.value.length) {
        return;
      }
      var posting = {
        // id: this.id,
        comment: this.comment
      };
      axios.post("http://127.0.0.1:5000/add", posting).then(function(res) {
        // フォーム要素を空にする
        comment.value = "";
        // todos リストへ pushする。
        // 例：{ 新しいID, コメント }
        this.entries.push({
          id: id.value,
          comment: comment.value
        });
      });
    },
    // ToDoリスト削除の処理
    doRemove(entry) {
      var index = this.entries.indexOf(entry);
      this.entries.splice(index, 1);
      var posting = {
        id: this.id
      };
      axios
        .post("http://127.0.0.1:5000/delete/" + this.id, posting)
        .then(function(res) {
          console.log(res.data);
        });
    },
    // ToDoリスト削除の処理
    doAllRemove(entry) {
      var index = this.entries.indexOf(entry);
      this.entries.splice(index, 1);
      var posting = {
        id: this.id
      };
      axios
        .post("http://127.0.0.1:5000/all-delete", posting)
        .then(function(res) {
          console.log(res.data);
        });
    }
  }
};
</script>
<style>
* {
  box-sizing: border-box;
}

#app {
  max-width: 640px;
  margin: 0 auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  border-bottom: 2px solid #0099e4;
  /*#d31c4a */
  color: #0099e4;
}

th,
th {
  padding: 0 8px;
  line-height: 40px;
}

thead th.id {
  width: 50px;
}

thead th.state {
  width: 100px;
}

thead th.button {
  width: 60px;
}

tbody td.button,
tbody td.state {
  text-align: center;
}

tbody tr td,
tbody tr th {
  border-bottom: 1px solid #ccc;
  transition: all 0.4s;
}

tbody tr.done td,
tbody tr.done th {
  background: #f8f8f8;
  color: #bbb;
}

tbody tr:hover td,
tbody tr:hover th {
  background: #f4fbff;
}

button {
  border: none;
  border-radius: 20px;
  line-height: 24px;
  padding: 0 8px;
  background: #0099e4;
  color: #fff;
  cursor: pointer;
}
.div {
  background: rgb(175, 175, 175);
}
</style>
