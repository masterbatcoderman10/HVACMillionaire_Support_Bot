var domain = 'https://chat.okradatacom.com/';
var cssId = 'myCss';  // you could encode the css path itself to generate id..
if (!document.getElementById(cssId))
{
    var head  = document.getElementsByTagName('head')[0];
    var link  = document.createElement('link');
    link.id   = cssId;
    link.rel  = 'stylesheet';
    link.type = 'text/css';
    link.href = domain+'static/style.css';
    link.media = 'all';
    head.appendChild(link);
}
var chatboxDiv = document.createElement('div');chatboxDiv.classList = "chatbox";
var chatbox__support = document.createElement('div');chatbox__support.classList = "chatbox__support";
var chatbox__header = document.createElement('div'); chatbox__header.classList="chatbox__header";
var chatbox__image__header = document.createElement('div'); chatbox__image__header.classList="chatbox__image--header";
var chatbot__header_agent_img = document.createElement('img'); chatbot__header_agent_img.classList = "chatbot__header-agent";chatbot__header_agent_img.alt="image";chatbot__header_agent_img.src=domain+'static/images/chatbot-agent.png';
chatbox__image__header.appendChild(chatbot__header_agent_img);
chatbox__header.appendChild(chatbox__image__header);
var chatbox__content__header = document.createElement('div'); chatbox__content__header.classList="chatbox__content--header";
var chatbox__heading__header = document.createElement('h4'); chatbox__heading__header.classList="chatbox__heading--header";chatbox__heading__header.innerText="Chat support";
var chatbox__description__header_1 = document.createElement('p'); chatbox__description__header_1.classList="chatbox__description--header";chatbox__description__header_1.innerText="Hi. This is BCRemit support,";
var chatbox__description__header_2 = document.createElement('p'); chatbox__description__header_2.classList="chatbox__description--header";
chatbox__description__header_2.innerText="how can I help you today?";
chatbox__content__header.appendChild(chatbox__heading__header);
chatbox__content__header.appendChild(chatbox__description__header_1);
chatbox__content__header.appendChild(chatbox__description__header_2);
chatbox__header.appendChild(chatbox__content__header);
chatbox__support.appendChild(chatbox__header);
var liveagentbutton = document.createElement('a');
liveagentbutton.classList = "liveagentbutton";
liveagentbutton.style="display:none;";
chatbox__support.appendChild(liveagentbutton);
var chatbox__messages = document.createElement('div');
chatbox__messages.classList="chatbox__messages";
var messages__item__operator = document.createElement('div');
messages__item__operator.classList = "messages__item messages__item--operator remove-after-user-details";
var msgsndr_message_form__hidden = document.createElement('form');
msgsndr_message_form__hidden.classList = 'msgsndr_message-form--hidden';
var TextInput_1 = document.createElement('div');
TextInput_1.classList = 'TextInput';
TextInput_1.innerHTML = '<label for="msgsndr_name">Name</label><input name="name" type="text" class="TextInput__Input" id="msgsndr_name" required="">';
msgsndr_message_form__hidden.appendChild(TextInput_1);
var TextInput_2 = document.createElement('div');
TextInput_2.classList = 'TextInput';
TextInput_2.innerHTML = '<label for="msgsndr_mobile_phone">Mobile Phone</label><div><select name="countryCode" id="countryCode" class="countrycode"><option value="+44" Selected>+44</option><option value="+63">+63</option><optgroup label="Other countries"><option value="+213">+213</option><option value="+376">+376</option><option value="+244">+244</option><option value="+1264">+1264</option><option value="+1268">+1268</option><option value="+54">+54</option><option value="+374">+374</option><option value="+297">+297</option><option value="+61">+61</option><option value="+43">+43</option><option value="+994">+994</option><option value="+1242">+1242</option><option value="+973">+973</option><option value="+880">+880</option><option value="+1246">+1246</option><option value="+375">+375</option><option value="+32">+32</option><option value="+501">+501</option><option value="+229">+229</option><option value="+1441">+1441</option><option value="+975">+975</option><option value="+591">+591</option><option value="+387">+387</option><option value="+267">+267</option><option value="+55">+55</option><option value="+673">+673</option><option value="+359">+359</option><option value="+226">+226</option><option value="+257">+257</option><option value="+855">+855</option><option value="+237">+237</option><option value="+1">+1</option><option value="+238">+238</option><option value="+1345">+1345</option><option value="+236">+236</option><option value="+56">+56</option><option value="+86">+86</option><option value="+57">+57</option><option value="+269">+269</option><option value="+242">+242</option><option value="+682">+682</option><option value="+506">+506</option><option value="+385">+385</option><option value="+53">+53</option><option value="+90392">+90392</option><option value="+357">+357</option><option value="+42">+42</option><option value="+45">+45</option><option value="+253">+253</option><option value="+1809">+1809</option><option value="+1809">+1809</option><option value="+593">+593</option><option value="+20">+20</option><option value="+503">+503</option><option value="+240">+240</option><option value="+291">+291</option><option value="+372">+372</option><option value="+251">+251</option><option value="+500">+500</option><option value="+298">+298</option><option value="+679">+679</option><option value="+358">+358</option><option value="+33">+33</option><option value="+594">+594</option><option value="+689">+689</option><option value="+241">+241</option><option value="+220">+220</option><option value="+7880">+7880</option><option value="+49">+49</option><option value="+233">+233</option><option value="+350">+350</option><option value="+30">+30</option><option value="+299">+299</option><option value="+1473">+1473</option><option value="+590">+590</option><option value="+671">+671</option><option value="+502">+502</option><option value="+224">+224</option><option value="+245">+245</option><option value="+592">+592</option><option value="+509">+509</option><option value="+504">+504</option><option value="+852">+852</option><option value="+36">+36</option><option value="+354">+354</option><option value="+91">+91</option><option value="+62">+62</option><option value="+98">+98</option><option value="+964">+964</option><option value="+353">+353</option><option value="+972">+972</option><option value="+39">+39</option><option value="+1876">+1876</option><option value="+81">+81</option><option value="+962">+962</option><option value="+7">+7</option><option value="+254">+254</option><option value="+686">+686</option><option value="+850">+850</option><option value="+82">+82</option><option value="+965">+965</option><option value="+996">+996</option><option value="+856">+856</option><option value="+371">+371</option><option value="+961">+961</option><option value="+266">+266</option><option value="+231">+231</option><option value="+218">+218</option><option value="+417">+417</option><option value="+370">+370</option><option value="+352">+352</option><option value="+853">+853</option><option value="+389">+389</option><option value="+261">+261</option><option value="+265">+265</option><option value="+60">+60</option><option value="+960">+960</option><option value="+223">+223</option><option value="+356">+356</option><option value="+692">+692</option><option value="+596">+596</option><option value="+222">+222</option><option value="+269">+269</option><option value="+52">+52</option><option value="+691">+691</option><option value="+373">+373</option><option value="+377">+377</option><option value="+976">+976</option><option value="+1664">+1664</option><option value="+212">+212</option><option value="+258">+258</option><option value="+95">+95</option><option value="+264">+264</option><option value="+674">+674</option><option value="+977">+977</option><option value="+31">+31</option><option value="+687">+687</option><option value="+64">+64</option><option value="+505">+505</option><option value="+227">+227</option><option value="+234">+234</option><option value="+683">+683</option><option value="+672">+672</option><option value="+670">+670</option><option value="+47">+47</option><option value="+968">+968</option><option value="+680">+680</option><option value="+507">+507</option><option value="+675">+675</option><option value="+595">+595</option><option value="+51">+51</option><option value="+48">+48</option><option value="+351">+351</option><option value="+1787">+1787</option><option value="+974">+974</option><option value="+262">+262</option><option value="+40">+40</option><option value="+7">+7</option><option value="+250">+250</option><option value="+378">+378</option><option value="+239">+239</option><option value="+966">+966</option><option value="+221">+221</option><option value="+381">+381</option><option value="+248">+248</option><option value="+232">+232</option><option value="+65">+65</option><option value="+421">+421</option><option value="+386">+386</option><option value="+677">+677</option><option value="+252">+252</option><option value="+27">+27</option><option value="+34">+34</option><option value="+94">+94</option><option value="+290">+290</option><option value="+1869">+1869</option><option value="+1758">+1758</option><option value="+249">+249</option><option value="+597">+597</option><option value="+268">+268</option><option value="+46">+46</option><option value="+41">+41</option><option value="+963">+963</option><option value="+886">+886</option><option value="+7">+7</option><option value="+66">+66</option><option value="+228">+228</option><option value="+676">+676</option><option value="+1868">+1868</option><option value="+216">+216</option><option value="+90">+90</option><option value="+7">+7</option><option value="+993">+993</option><option value="+1649">+1649</option><option value="+688">+688</option><option value="+256">+256</option><option value="+380">+380</option><option value="+971">+971</option><option value="+1">+1</option><option value="+598">+598</option><option value="+7">+7</option><option value="+678">+678</option><option value="+379">+379</option><option value="+58">+58</option><option value="+84">+84</option><option value="+1284">+1284</option><option value="+1340">+1340</option><option value="+681">+681</option><option value="+969">+969</option><option value="+967">+967</option><option value="+260">+260</option><option value="+263">+263</option></optgroup></select><input name="phone" type="text" class="TextInput__Input TextInput__Input_phone" id="msgsndr_mobile_phone" required="" autocomplete="off" data-intl-tel-input-id="0"></div><div class="TextInput__Bar"></div>';
msgsndr_message_form__hidden.appendChild(TextInput_2);
var TextInput_3 = document.createElement('div');
TextInput_3.classList = 'TextInput';
TextInput_3.innerHTML = '<label for="msgsndr_e-mail">E-mail</label><input name="email" type="email" class="TextInput__Input" id="msgsndr_e-mail" required="">';
msgsndr_message_form__hidden.appendChild(TextInput_3);
messages__item__operator.appendChild(msgsndr_message_form__hidden);
chatbox__messages.appendChild(messages__item__operator);
var messages__item__visitor = document.createElement('div');
messages__item__visitor.classList = "messages__item messages__item--visitor remove-after-user-details";
messages__item__visitor.innerText= "Please fill your details below: -";
chatbox__messages.appendChild(messages__item__visitor);
chatbox__support.appendChild(chatbox__messages);
var chatbox__footer = document.createElement('chatbox__footer');
chatbox__footer.classList="chatbox__footer";
chatbox__footer.innerHTML='<p id="typing_text" style="font-family: Nunito, sans-serif; position: absolute; top: -18px; font-size: 12px; left: 45px; display: none;">Typing...</p><div class="intro-part" style="width: 100%;"><button class="chatbox__send--footer user_register_button" id="submitDetailsButton" style="width: 100%;box-shadow: 1px 1px 2px 1px rgba(0, 0, 0, .2);background-color: transparent;padding: 10px 10px;border: none; cursor: pointer;">Submit details</button></div><div class="chat-part" style="width: 100%; display: none;"><input type="text" name="user-input" class="chat-input-text" placeholder="Write a message..."><button class="chatbox__send--footer send__button">Send</button></div>';
chatbox__support.appendChild(chatbox__footer);
chatboxDiv.appendChild(chatbox__support);
var chatbox__button = document.createElement('div');chatbox__button.classList = "chatbox__button";
var chatbox__button_button = document.createElement('button');
var chatbox__button_img = document.createElement('img');chatbox__button_img.src=domain+'static/images/chatbox-icon-blue.svg';
chatbox__button_button.appendChild(chatbox__button_img);
chatbox__button.appendChild(chatbox__button_button);
chatboxDiv.appendChild(chatbox__button);

setTimeout(function(){
    var jsId1 = 'myJs1';  // you could encode the css path itself to generate id..
    if (!document.getElementById(jsId1))
    {
        var head  = document.getElementsByTagName('head')[0];
        var link  = document.createElement('script');
        link.id   = jsId1;
        link.type = 'text/javascript';
        link.src = domain+'static/jquery.min.js';
        head.appendChild(link);
    }   
    document.body.appendChild(chatboxDiv);
}, 1000)

setTimeout(function(){    
    var jsId2 = 'myJs2';  // you could encode the css path itself to generate id..
    if (!document.getElementById(jsId2))
    {
        var head  = document.getElementsByTagName('head')[0];
        var link  = document.createElement('script');
        link.id   = jsId2;
        link.type = 'text/javascript';
        link.src = domain+'static/typing.js';
        head.appendChild(link);
    }
    
    var jsId3= 'myJs3';  // you could encode the css path itself to generate id..
    if (!document.getElementById(jsId3))
    {
        var head  = document.getElementsByTagName('head')[0];
        var link  = document.createElement('script');
        link.id   = jsId3;
        link.type = 'text/javascript';
        link.src = domain+'static/appchatbot31.js';
        head.appendChild(link);
    }   
}, 2000)

