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
            <button v-on:click="doDelete(entry.id)">削除</button>
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
      <button v-on:click="doAllDelete()">すべて削除</button>
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
      // Todoリストデータ用のカラ配列をdataオプションに登録する。
      entries: [],
      comment: "",
      // ベースURLの設定
      baseUrl: "http://127.0.0.1:5000/"
    };
  },
  created() {
    this.getTodo();
  },
  methods: {
    // -- 使用するメソッドはここへ -- //
    getIndex: function(value, arr, prop) {
      for (var i = 0; i < arr.length; i++) {
        if (arr[i][prop] === value) {
          return i;
        }
      }
      return -1; //値が存在しなかったとき
    },
    // データベースからTodoリスト一覧を呼んでくる。
    async getTodo() {
      try {
        let response = await axios.get(this.baseUrl + "get_all_todos");
        this.entries = response.data;
      } catch (error) {
        console.log(error);
      }
    },
    // Todoリスト追加の処理
    async doAdd() {
      // コメント入力が空なら何もしない。
      if (!this.comment) {
        return;
      }
      try {
        let params = {
          comment: this.comment
        };
        await axios.post(this.baseUrl + "add", params);
        // this.getTodo();

        this.entries.push({
          id: this.id,
          comment: this.comment
        });
        this.comment = "";
      } catch (error) {
        console.log(error);
      }
    },
    // Todoリスト削除の処理
    async doDelete(delete_id) {
      try {
        await axios.post(this.baseUrl + "delete/" + delete_id);
        // this.getTodo();

        // var index = this.entries.indexOf({ id: delete_id });
        var index = this.getIndex(delete_id, this.entries, "id");
        console.log(index);
        this.entries.splice(index, 1);
      } catch (error) {
        console.log(error);
      }
    },
    async doDeleteAll() {
      // Todoリスト全削除の処理
      try {
        await axios.post(this.baseUrl + "all-delete");
        this.getTodo();
      } catch (error) {
        console.log(error);
      }
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
