

const COOKIE_NAME = "consent-ads";
const CONSENT_STORAGE = "consent_marketing";
const CONSENT_ITEMS = ["consent_marketing","ad_storage", "analytics_storage", "functionality_storage", "personalization_storage", "security_storage"];
const CONSENT_GRANTED = "granted";
const CONSENT_DENIED = "denied";
const LOCAL_STORAGE = "localStorage";
const SESSION_STORAGE = "sessionStorage";
const CONSENT_STORAGE_DURATION = 365; // Days
const COOKIE_CONSENT_MODAL_SELECTOR = 'cookie-consent-modal';
const COOKIE_CONTENT_BTN_SELECTOR = 'cookie-content-btn';
const AD_CLIENT = "ca-pub-7624615584108748";
const AD_SLOT = "6056470096";
const AD_FORMAT = "auto";
const data = [
    {
        'ad-format': 'auto','ad-client': "ca-pub-7624615584108748","ad-slot": "6056470096"
    },
    {
        'ad-format': 'autorelaxed','ad-client': "ca-pub-7624615584108748","ad-slot": "5865333179"
    }
];

function load_gtm(){
    (function(w,d,s,l,i){
        w[l]=w[l]||[];
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

function resetStorage(){
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

function onUserGranted(){
    if(!storageAvailable(LOCAL_STORAGE)){
        console.log("%s is not available", LOCAL_STORAGE);
        return ;
    }
    CONSENT_ITEMS.forEach(entry =>{
        localStorage.setItem(entry, CONSENT_GRANTED);
        Cookies.set(entry, CONSENT_GRANTED, {sameSite:"Lax", expires: CONSENT_STORAGE_DURATION});
    });
    Cookies.set(COOKIE_NAME, CONSENT_GRANTED, {sameSite:"Lax", expires: CONSENT_STORAGE_DURATION});
}

function load_cookie_consent(callback){
    if(!storageAvailable(LOCAL_STORAGE)){
        console.log("%s is not available", LOCAL_STORAGE);
        return ;
    }
    let consent_storage = localStorage.getItem(CONSENT_STORAGE);
    if(consent_storage != null && consent_storage == CONSENT_GRANTED){
        return true;
    }

    let modal = document.getElementById(COOKIE_CONSENT_MODAL_SELECTOR);
    if(modal == null){
        return false;
    }
    
    let  accep_btn = document.getElementById(COOKIE_CONTENT_BTN_SELECTOR);
    accep_btn.addEventListener('click', event =>{
        modal.style.display = 'none';
        if(callback){
            callback();
        }
    });
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
    load_gtm();
    const updateConsentState = require('updateConsentState');
    (adsbygoogle = window.adsbygoogle || []).push({});
    load_cookie_consent(onUserGranted);
    console.log("loaded adsense");
});
    