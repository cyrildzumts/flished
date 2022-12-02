

const COOKIE_NAME = "consent-ads";
const CONSENT_STORAGE = "consent_marketing";
const CONSENT_ITEMS = ["consent_marketing","ad_storage", "analytics_storage", "functionality_storage", "personalization_storage", "security_storage"];
const CONSENT_GRANTED = "granted";
const CONSENT_DENIED = "denied";
const LOCAL_STORAGE = "localStorage";
const SESSION_STORAGE = "sessionStorage";
const GTM_ID = "GTM-P59WJQQ";
const TAG_ID = "G-NQPSEMG1ZR";
const CONSENT_STORAGE_DURATION = 365; // Days
const CONSENT_DENIED_STORAGE_DURATION = 7; // Days
const COOKIE_CONSENT_MODAL_SELECTOR = 'cookie-consent-modal';
const COOKIE_GRANTED_BTN_SELECTOR = 'cookie-granted-btn';
const COOKIE_DENIED_BTN_SELECTOR = 'cookie-denied-btn';
const COOKIE_PREFERENCE_BTN_SELECTOR = 'cookie-preference-btn';
const AD_CLIENT = "ca-pub-7624615584108748";
const AD_SLOT = "6056470096";
const AD_FORMAT = "auto";
let DATALAYER = undefined;
const data = [
    {
        'ad-format': 'auto','ad-client': "ca-pub-7624615584108748","ad-slot": "6056470096"
    },
    {
        'ad-format': 'autorelaxed','ad-client': "ca-pub-7624615584108748","ad-slot": "5865333179"
    }
];


function gtag(){
    DATALAYER.push(arguments);
}

function gtag_event(obj){
    DATALAYER.push(obj);
}

function load_gtm(){
    (function(w,d,s,l,i){
        DATALAYER = w[l]=w[l]||[];
        set_default_consent();
        w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});
        var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';
        j.async=true;
        j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;
        f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-P59WJQQ');
    
}



function storageAvailable(type) {
    let storage;
    try {
        storage = window[type];
        const x = '__storage_test__';
        storage.setItem(x, x);
        storage.removeItem(x);
        return true;
    }
    catch (e) {
        return e instanceof DOMException && (
            // everything except Firefox
            e.code === 22 ||
            // Firefox
            e.code === 1014 ||
            // test name field too, because code might not be present
            // everything except Firefox
            e.name === 'QuotaExceededError' ||
            // Firefox
            e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
            // acknowledge QuotaExceededError only if there's something already stored
            (storage && storage.length !== 0);
    }
}

function reset_storage(){
    if(!storageAvailable(LOCAL_STORAGE)){
        console.log("%s is not available", LOCAL_STORAGE);
        return ;
    }
    CONSENT_ITEMS.forEach(entry =>{
        localStorage.removeItem(entry);
        Cookies.remove(entry);
    });
    Cookies.remove(COOKIE_NAME);
}

function set_default_consent(){
    let tagObject = {};
    CONSENT_ITEMS.forEach(entry =>{
        tagObject[entry] = CONSENT_DENIED;
    });
    let dataLayerVariables = {
        'essentialConsent':"denied",
        'performanceConsent' :"denied",
        'analyticsConsent':"denied",
        'advertisingConsent': 'denied',
    };
    gtag('consent', 'default', tagObject);
    gtag_event(dataLayerVariables);
}

function watcher_default(){
    window.addEventListener("load", function(ev){
        console.log("Flished Tag manager loaded ...");
      });
      window.addEventListener('message', function (ev) {
      if (ev.data.message==='consent_given') {
        console.log(ev.data.consentStatuses);
        ev.data.consentStatuses&&Object.keys(ev.data.consentStatuses).forEach(function (category) {
            if (ev.data.consentStatuses[category]) {
                dataLayer.push({
                'event': 'userPrefUpdate',
                'cookieConsent': category
                });
            }
            });
        }
      });
}

function onUserGranted(){
    if(!storageAvailable(LOCAL_STORAGE)){
        console.log("%s is not available", LOCAL_STORAGE);
        return ;
    }
    let tagObject = {

    };
    let consents = document.querySelectorAll('.js-essential');
    consents.forEach((input) =>{
        tagObject[input.name] = input.value;
        localStorage.setItem(input.name, input.value);
        Cookies.set(input.name, input.value, {sameSite:"Lax", expires: input.checked ? CONSENT_STORAGE_DURATION : CONSENT_DENIED_STORAGE_DURATION});
    });
    /*
    CONSENT_ITEMS.forEach(entry =>{
        localStorage.setItem(entry, CONSENT_GRANTED);
        Cookies.set(entry, CONSENT_GRANTED, {sameSite:"Lax", expires: CONSENT_STORAGE_DURATION});
        tagObject[entry] = CONSENT_GRANTED;
    });
    */
    Cookies.set(COOKIE_NAME, CONSENT_GRANTED, {sameSite:"Lax", expires: CONSENT_STORAGE_DURATION});
    let dataLayerVariables = {
        'essentialConsent':"granted",
        'performanceConsent' :"granted",
        'analyticsConsent':"granted",
        'advertisingConsent': 'granted',
    };
    gtag('consent', 'update', tagObject);
    gtag_event({'event':'gtm.init_consent'});
    gtag_event(dataLayerVariables);
    gtag_event({'event':'analyticsUpdate'});
    gtag_event({'event':'advertisingUpdate' });
    gtag_event({'event':'performanceUpdate' });
    gtag_event({'event':'essentialUpdate' });
    gtag_event({'event': 'flished_consent_given'});
}

function onUserDenied(){
    if(!storageAvailable(LOCAL_STORAGE)){
        console.log("%s is not available", LOCAL_STORAGE);
        return ;
    }
    let tagObject = {};
    CONSENT_ITEMS.forEach(entry =>{
        localStorage.setItem(entry, CONSENT_DENIED);
        Cookies.set(entry, CONSENT_DENIED, {sameSite:"Lax", expires: CONSENT_DENIED_STORAGE_DURATION});
        tagObject[entry] = CONSENT_DENIED;
    });
    Cookies.set(COOKIE_NAME, CONSENT_DENIED, {sameSite:"Lax", expires: CONSENT_DENIED_STORAGE_DURATION});
    tagObject['consent'] = 'update';
    gtag(tagObject);
    gtag({'event': 'essentialUpdate', 'essentialConsent':"denied"});
    gtag({'event': 'performanceUpdate', 'performanceConsent':"denied"});
    gtag({'event': 'analyticsUpdate', 'analyticsConsent':"denied"});
}

function load_cookie_consent(callback){
    if(!storageAvailable(LOCAL_STORAGE)){
        console.log("%s is not available", LOCAL_STORAGE);
        return ;
    }
    let consent = Cookies.get(COOKIE_NAME);
    
    if(consent != undefined){
        if(consent == CONSENT_GRANTED){
            onUserGranted();
        }
        return true;
    }
    reset_storage();

    let modal = document.getElementById(COOKIE_CONSENT_MODAL_SELECTOR);
    if(modal == null){
        return false;
    }
    
    let  accep_btn = document.getElementById(COOKIE_GRANTED_BTN_SELECTOR);
    let  denied_btn = document.getElementById(COOKIE_DENIED_BTN_SELECTOR);
    let  reset_btn = document.getElementById(COOKIE_DENIED_BTN_SELECTOR);
    let  preference_btn = document.getElementById(COOKIE_PREFERENCE_BTN_SELECTOR);
    
    accep_btn.addEventListener('click', event =>{
        modal.style.display = 'none';
        if(callback){
            callback();
        }
    });
    if(denied_btn){
        denied_btn.addEventListener('click', event =>{
            modal.style.display = 'none';
            onUserDenied();
        });
    }
    if(reset_btn){
        reset_btn.addEventListener('click', event =>{
            modal.style.display = 'none';
            reset_storage();
        });
    }
    if(preference_btn){
        let preference = document.getElementById(preference_btn.dataset.toggle);
        preference_btn.addEventListener('click', event =>{
            if(preference.style.display == ''){
                preference.style.display = "block";
            }else{
                preference.style.display = "";
            }
        });
    }
    if(window){
        $(window).click(function(eventModal){
            if(eventModal.target == modal){
                modal.style.display = "none";
            }
        });
        modal.style.display = 'flex';
    }
}

window.addEventListener('load',(event) =>{
    DATALAYER = window.dataLayer = window.dataLayer || [];
    //reset_storage();
    load_gtm();
    (adsbygoogle = window.adsbygoogle || []).push({});
    load_cookie_consent(onUserGranted);
    console.log("loaded adsense");
});
    