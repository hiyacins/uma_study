<template>
  <v-card>
    <v-card-title>
      <h2>スタッフ管理</h2>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="messages"
      sort-by="id"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark class="mb-2" v-on="on"
                >新規作成</v-btn
              >
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.id"
                        label="ID"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.name"
                        label="名前"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.priority"
                        label="優先順位"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-file-input
                        v-model="editedItem.image"
                        chips
                        multiple
                        label="画像"
                      ></v-file-input>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close"
                  >キャンセル</v-btn
                >
                <v-btn color="blue darken-1" text @click="save">保存</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)">
          mdi-pencil
        </v-icon>
        <v-icon small @click="deleteItem(item)">
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize">Reset</v-btn>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    dialog: false,
    headers: [
      {
        text: "ID",
        align: "start",
        sortable: false,
        value: "id",
      },
      { text: "名前", value: "name" },
      { text: "画像", value: "image" },
      { text: "優先順位", value: "priority" },
      { text: "編集/削除", value: "actions", sortable: false },
    ],
    messages: [],
    editedIndex: -1,
    editedItem: {
      id: "",
      name: "",
      image: "",
      priority: "",
    },
    defaultItem: {
      id: "",
      name: "",
      image: "",
      priority: "",
    },
  }),
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "新規メッセージ" : "編集";
    },
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
  },
  created() {
    this.initialize();
  },
  methods: {
    initialize() {
      this.messages = [
        {
          id: 7010,
          name: "佐藤一郎",
          image: "",
          priority: 1,
        },
        {
          id: 7020,
          name: "佐藤二郎",
          image: "",
          priority: 2,
        },
        {
          id: 7030,
          name: "佐藤四郎",
          image: "",
          priority: 3,
        },
      ];
    },
    editItem(item) {
      this.editedIndex = this.messages.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    deleteItem(item) {
      const index = this.messages.indexOf(item);
      confirm("削除しても良いですか？") && this.messages.splice(index, 1);
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.messages[this.editedIndex], this.editedItem);
      } else {
        this.messages.push(this.editedItem);
      }
      this.close();
    },
  },
};
</script>
