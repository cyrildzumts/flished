

const COOKIE_NAME = "consent-ads";
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

function load_sense_tools(user_accepted){
    if(!user_accepted){
        return;
    }
    (function(w,d,s,l,i){
        w[l]=w[l]||[];
        w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});
        var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';
        j.async=true;
        j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;
        f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-P59WJQQ');
    if(adsbygoogle){
        (adsbygoogle = window.adsbygoogle || []).push({});
    }
    console.log("Sense tool loaded");
}

function load_cookie_consent(){
    let cookie = Cookies.get(COOKIE_NAME);
    if(cookie && cookie == "accepted"){
        load_sense_tools(true);
        console.log("User has already accepted ads");
        return;
    }
    console.log("User has not already accepted ads");
    let modal = document.getElementById(COOKIE_CONSENT_MODAL_SELECTOR);
    if(modal == null){
        return;
    }
    
    let  accep_btn = document.getElementById(COOKIE_CONTENT_BTN_SELECTOR);
    accep_btn.addEventListener('click', event =>{
        modal.style.display = 'none';
        Cookies.set(COOKIE_NAME, "accepted", {secure: false, sameSite:"Lax"});
        load_sense_tools(true);
        console.log("Cookie usage consented by the user");
    });
    if(window){
        $(window).click(function(eventModal){
            if(eventModal.target == modal){
                modal.style.display = "none";
            }
        });
        modal.style.display = 'flex';
    }
    console.log("Cookie consent loaded");
}
    window.addEventListener('load', event=>{
        load_cookie_consent();
        console.log("libsense module ready");
    })