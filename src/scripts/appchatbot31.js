class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
      userRegisterButton: document.querySelector(".user_register_button"),
      liveAgentButton: document.querySelector(".liveagentbutton"),
      api_url: "http://localhost:3000",
    };

    this.state = false;
    this.messages = [];
    this.data = {};
  }

  display() {
    const {
      openButton,
      chatBox,
      sendButton,
      userRegisterButton,
      liveAgentButton,
    } = this.args;

    openButton.addEventListener("click", () => this.toggleState(chatBox));

    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    userRegisterButton.addEventListener("click", () =>
      this.onRegisterButton(chatBox)
    );

    liveAgentButton.addEventListener("click", () =>
      this.onliveAgentButton(chatBox, this)
    );

    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }

  toggleState(chatbox) {
    this.state = !this.state;

    // show or hides the box
    if (this.state) {
      chatbox.classList.add("chatbox--active");
    } else {
      chatbox.classList.remove("chatbox--active");
    }
  }

  onSendButton(chatbox) {
    var textField = chatbox.querySelector(".chat-input-text");
    let text1 = textField.value;
    if (text1 === "") {
      return;
    }
    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML =
      '<div class="messages__item messages__item--operator">' +
      text1 +
      "</div>" +
      chatmessage.innerHTML;
    setTimeout(function () {
      $("#typing_text").show();
    }, 2000);
    let msg1 = { name: "User", message: text1 };
    this.messages.push(msg1);
    textField.value = "";
    fetch(`${this.args.api_url}/chatbot`, {
      method: "POST",
      body: JSON.stringify({ "user-input": text1 }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        let msg2 = { name: "Sam", message: r.response };
        this.messages.push(msg2);
        this.updateChatTextExtended(chatbox, r.response);
      })
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatbox);
        textField.value = "";
      });
  }

  updateChatTextExtended(chatbox, messageResponse) {
    const chatmessage = chatbox.querySelector(".chatbox__messages");
    if (messageResponse.search("Open a support ticket") != -1) {
      messageResponse = messageResponse.replace(
        "1. Open a support ticket",
        '<a class="liveagentbutton support-ticket" ">Open a support ticket</a>'
      );
      messageResponse = messageResponse.replace(
        "2. Get a call back",
        '<a class="liveagentbutton get-call-back" >Get a call back</a>'
      );
      messageResponse = messageResponse.replace(
        "3. Chat with SMS",
        '<a class="liveagentbutton chat-with-sms" >Chat with SMS</a>'
      );
      messageResponse = messageResponse.replace(
        "4. Chat with email",
        '<a class="liveagentbutton chat-with-email">Chat with email</a>'
      );
      chatmessage.innerHTML =
        '<div class="messages__item messages__item--visitor">' +
        messageResponse +
        "</div>" +
        chatmessage.innerHTML;
      $("#typing_text").hide();
      document.addEventListener("click", function (event, chatbox) {
        // Check if the clicked element has the class "button"
        var text1;
        if (event.target.classList.contains("support-ticket")) {
          chatmessage.innerHTML =
            '<div class="messages__item messages__item--operator">Open a support ticket</div>' +
            chatmessage.innerHTML;
          text1 = "Open a support ticket";
        } else if (event.target.classList.contains("get-call-back")) {
          chatmessage.innerHTML =
            '<div class="messages__item messages__item--operator">Get a call back</div>' +
            chatmessage.innerHTML;
          text1 = "Get a call back";
        } else if (event.target.classList.contains("chat-with-sms")) {
          chatmessage.innerHTML =
            '<div class="messages__item messages__item--operator">Chat with SMS</div>' +
            chatmessage.innerHTML;
          text1 = "Chat with SMS";
        } else if (event.target.classList.contains("chat-with-email")) {
          chatmessage.innerHTML =
            '<div class="messages__item messages__item--operator">Chat with email</div>' +
            chatmessage.innerHTML;
          text1 = "Chat with email";
        }
        setTimeout(function () {
          $("#typing_text").show();
        }, 2000);
        let msg1 = { name: "User", message: text1 };
        // this.messages.push(msg1);

        fetch(`${this.args.api_url}/chatbot`, {
          method: "POST",
          body: JSON.stringify({ "user-input": text1 }),
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((r) => r.json())
          .then((r) => {
            let msg2 = { name: "Sam", message: r.response };
            // chatbox.messages.push(msg2);
            chatmessage.innerHTML =
              '<div class="messages__item messages__item--visitor" id="current"></div>' +
              chatmessage.innerHTML;
            if ($("#current").length > 0) {
              $("#current").teletype({
                text: [r.response],
              });
              // $("#current").html(holdMessage);
              $("#current").removeAttr("id");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            // chatbox.updateChatText(chatbox)
            textField.value = "";
          });
      });
    } else if (
      messageResponse.search("Bumuo ng isang support ticket") != -1 ||
      messageResponse.search("Buksan ang isang support ticket") != -1 ||
      messageResponse.search("Magbukas ng support ticket") != -1
    ) {
      messageResponse = messageResponse.replace(
        "1. Bumuo ng isang support ticket",
        '<a class="liveagentbutton support-ticket" ">Bumuo ng isang support ticket</a>'
      );
      messageResponse = messageResponse.replace(
        "1. Buksan ang isang support ticket",
        '<a class="liveagentbutton support-ticket" ">Buksan ang isang support ticket</a>'
      );
      messageResponse = messageResponse.replace(
        "1. Magbukas ng support ticket",
        '<a class="liveagentbutton support-ticket" ">Magbukas ng support ticket</a>'
      );
      messageResponse = messageResponse.replace(
        "2. Maghintay ng tawag mula sa amin",
        '<a class="liveagentbutton get-call-back" >Maghintay ng tawag mula sa amin</a>'
      );
      messageResponse = messageResponse.replace(
        "2. Tawagan ka",
        '<a class="liveagentbutton get-call-back" >Tawagan ka</a>'
      );
      messageResponse = messageResponse.replace(
        "2. Tumawag para sa callback",
        '<a class="liveagentbutton get-call-back" >Tumawag para sa callback</a>'
      );
      messageResponse = messageResponse.replace(
        "2. Mag-request ng tawag balik",
        '<a class="liveagentbutton get-call-back" >Mag-request ng tawag balik</a>'
      );
      messageResponse = messageResponse.replace(
        "2. Magpa-tawag pabalik",
        '<a class="liveagentbutton get-call-back" >Magpa-tawag pabalik</a>'
      );
      messageResponse = messageResponse.replace(
        "2. Makakuha ng tawag pabalik",
        '<a class="liveagentbutton get-call-back" >Makakuha ng tawag pabalik</a>'
      );
      messageResponse = messageResponse.replace(
        "2. Tumawag muli",
        '<a class="liveagentbutton get-call-back" >Tumawag muli</a>'
      );
      messageResponse = messageResponse.replace(
        "2. Makakuha ng tawag balik",
        '<a class="liveagentbutton get-call-back" >Makakuha ng tawag balik</a>'
      );
      messageResponse = messageResponse.replace(
        "3. Makipag-chat gamit ang SMS",
        '<a class="liveagentbutton chat-with-sms" >Makipag-chat gamit ang SMS</a>'
      );
      messageResponse = messageResponse.replace(
        "3. Chat sa SMS",
        '<a class="liveagentbutton chat-with-sms" >Chat sa SMS</a>'
      );
      messageResponse = messageResponse.replace(
        "3. Mag-chat gamit ang SMS",
        '<a class="liveagentbutton chat-with-sms" >Mag-chat gamit ang SMS</a>'
      );
      messageResponse = messageResponse.replace(
        "3. Makipag-chat sa SMS",
        '<a class="liveagentbutton chat-with-sms" >Makipag-chat sa SMS</a>'
      );
      messageResponse = messageResponse.replace(
        "4. Makipag-chat gamit ang email",
        '<a class="liveagentbutton chat-with-email">Makipag-chat gamit ang email</a>'
      );
      messageResponse = messageResponse.replace(
        "4. Mag-chat gamit ang email",
        '<a class="liveagentbutton chat-with-email">Mag-chat gamit ang email</a>'
      );
      messageResponse = messageResponse.replace(
        "4. Chat sa email",
        '<a class="liveagentbutton chat-with-email">Chat sa email</a>'
      );
      messageResponse = messageResponse.replace(
        "4. Makipag-chat sa email",
        '<a class="liveagentbutton chat-with-email">Makipag-chat sa email</a>'
      );
      chatmessage.innerHTML =
        '<div class="messages__item messages__item--visitor">' +
        messageResponse +
        "</div>" +
        chatmessage.innerHTML;
      $("#typing_text").hide();
      document.addEventListener("click", function (event, chatbox) {
        var text1;
        if (event.target.classList.contains("support-ticket")) {
          chatmessage.innerHTML =
            '<div class="messages__item messages__item--operator">' +
            event.target.innerHTML +
            "</div>" +
            chatmessage.innerHTML;
        } else if (event.target.classList.contains("get-call-back")) {
          chatmessage.innerHTML =
            '<div class="messages__item messages__item--operator">' +
            event.target.innerHTML +
            "</div>" +
            chatmessage.innerHTML;
        } else if (event.target.classList.contains("chat-with-sms")) {
          chatmessage.innerHTML =
            '<div class="messages__item messages__item--operator">' +
            event.target.innerHTML +
            "</div>" +
            chatmessage.innerHTML;
        } else if (event.target.classList.contains("chat-with-email")) {
          chatmessage.innerHTML =
            '<div class="messages__item messages__item--operator">' +
            event.target.innerHTML +
            "</div>" +
            chatmessage.innerHTML;
        }
        text1 = event.target.innerHTML;
        setTimeout(function () {
          $("#typing_text").show();
        }, 2000);
        let msg1 = { name: "User", message: text1 };
        // this.messages.push(msg1);

        fetch(`${this.args.api_url}/chatbot`, {
          method: "POST",
          body: JSON.stringify({ "user-input": text1 }),
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((r) => r.json())
          .then((r) => {
            let msg2 = { name: "Sam", message: r.response };
            // chatbox.messages.push(msg2);
            chatmessage.innerHTML =
              '<div class="messages__item messages__item--visitor" id="current"></div>' +
              chatmessage.innerHTML;
            if ($("#current").length > 0) {
              $("#current").teletype({
                text: [r.response],
              });
              // $("#current").html(holdMessage);
              $("#current").removeAttr("id");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            // chatbox.updateChatText(chatbox)
            textField.value = "";
          });
      });
    } else {
      chatmessage.innerHTML =
        '<div class="messages__item messages__item--visitor" id="current"></div>' +
        chatmessage.innerHTML;
    }

    if ($("#current").length > 0) {
      $("#current").teletype({
        text: [messageResponse],
      });
      // $("#current").html(holdMessage);
      $("#current").removeAttr("id");
    }
  }

  updateChatText(chatbox) {
    var html = "";
    var holdMessage = "";
    // this.messages.slice().reverse().forEach(function(item, index) {
    //     if (item.name === "Sam")
    //     {
    //         holdMessage = item.message;
    //         html += '<div class="messages__item messages__item--visitor" id="current"></div>'
    //     }
    //     else
    //     {
    //         html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
    //     }
    //   });

    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
    if ($("#current").length > 0) {
      $("#current").teletype({
        text: [holdMessage],
      });
      // $("#current").html(holdMessage);
      $("#current").removeAttr("id");
    }
  }

  async onRegisterButton(chatbox) {
    // Extract user details from the form
    const name = document.getElementById("msgsndr_name").value;
    const email = document.getElementById("msgsndr_e-mail").value;
    var phone = document.getElementById("msgsndr_mobile_phone").value;
    const countrycode = document.getElementById("countryCode").value;

    // Check if any of the required fields is empty
    if (!name || !email || !phone) {
      alert("Please fill in all required fields.");
      return;
    }
    phone = countrycode + phone;

    const body = JSON.stringify({
      name: name,
      email: email,
      phone: phone,
    });

    const headers = {
      "Content-Type": "application/json",
    };

    const response = await fetch(`${this.args.api_url}/submit_details`, {
      method: "POST",
      body: body,
      headers: headers,
    });

    if (response.ok) {
      console.log("User details submitted successfully.");
      const response_data = await response.json();
      console.log(response_data);
      const contact_id = response_data.contact_id;
      this.data = Object.assign(this.data, { name, contact_id });
      console.log(this.data);
      chatbox.querySelector(".intro-part").style.display = "none";
      chatbox.querySelector(".chat-part").style.display = "block";
      chatbox.querySelectorAll(".remove-after-user-details").forEach((item) => {
        item.style.display = "none";
      });
      const greeting = `Hi ${name} how can I help you today`;
      this.messages.push({ name: "Sam", message: greeting });
      this.updateChatTextExtended(chatbox, greeting);
    } else {
      alert("Failed to submit user details.");
    }
  }

  typeString($target, str, cursor, delay, cb) {
    $target.html(function (_, html) {
      return html + str[cursor];
    });

    if (cursor < str.length - 1) {
      setTimeout(function () {
        typeString($target, str, cursor + 1, delay, cb);
      }, delay);
    } else {
      cb();
    }
  }
}

const chatbox = new Chatbox();
chatbox.display();
