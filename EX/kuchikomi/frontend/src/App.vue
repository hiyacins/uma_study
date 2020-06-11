<template>
  <v-app>
    <v-navigation-drawer app v-model="drawer" clipped>
      <v-container>
        <v-list dense nav>
          <v-list-item
            v-for="nav_list in nav_lists"
            :key="nav_list.name"
            :to="nav_list.link"
          >
            <v-list-item-icon>
              <v-icon>{{ nav_list.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ nav_list.name }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-group
            v-for="nav_config in nav_configs"
            :key="nav_config.name"
            :prepend-icon="nav_config.icon"
            no-action
            :append-icon="nav_config.lists ? undefined : ''"
          >
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>{{ nav_config.name }}</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item
              v-for="list in nav_config.lists"
              :key="list.name"
              :to="list.link"
            >
              <v-list-item-content>
                <v-list-item-title>{{ list.name }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-group>
        </v-list>
      </v-container>
    </v-navigation-drawer>

    <v-app-bar color="primary" dark app clipped-left>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>KUCHIKOMI</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="mb-1" v-on="on"
              >SNSを送信する</v-btn
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
                      v-model="editedItem.staff"
                      label="担当"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.name"
                      label="お客様の氏名"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedItem.tel"
                      label="送信先電話番号"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="100" md="100">
                    <v-textarea
                      v-model="editedItem.message"
                      label="メッセージ"
                    ></v-textarea>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close"
                >キャンセル</v-btn
              >
              <v-btn color="blue darken-1" text @click="send">SMSで送信</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar-items>
    </v-app-bar>
    <v-content>
      <router-view />
    </v-content>
    <!-- <v-footer color="primary" dark app>
      Vuetify
    </v-footer> -->
  </v-app>
</template>

<script>
// パーツ単位でファイルを分けたときimportでここに書く
//import HelloWorld from './components/HelloWorld';
export default {
  data() {
    return {
      drawer: null,
      dialog: false,
      nav_lists: [
        { name: "メッセージ", icon: "mdi-email", link: "/" },
        { name: "口コミ", icon: "mdi-chat", link: "/kuchikomi" },
        { name: "分析", icon: "mdi-chart-pie", link: "/analyze" },
        { name: "アンケート", icon: "mdi-view-dashboard", link: "/enquete" },
        {
          name: "DM一斉配信",
          icon: "mdi-bullhorn-outline",
          link: "/allmessage",
        },
      ],
      nav_configs: [
        {
          name: "設定",
          icon: "mdi-cog",
          lists: [
            {
              name: "スタッフ管理",
              link: "/staff",
            },
            {
              name: "QRコード設定",
              link: "/qrcode",
            },
            {
              name: "お問い合わせ先",
              link: "/contact",
            },
            {
              name: "請求書一覧",
              link: "/payment",
            },
            {
              name: "FAQ",
              link: "/faq",
            },
            {
              name: "利用ガイド",
              link: "/guide",
            },
            {
              name: "ログアウト",
              link: "/logout",
            },
          ],
        },
      ],
      editedItem: {
        staff: "",
        name: "",
        tel: "",
        message: "",
      },
    };
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
  },
  methods: {
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
    send() {
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
