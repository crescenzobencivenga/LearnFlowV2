// per il cambio lingua
function googleTranslateElementInit() {
    new google.translate.TranslateElement
    (
        {
            pageLanguage: 'en',
            includedLanguages: "en,it,es,ci,fr"
        },
        'google_translate_element'
    );
}