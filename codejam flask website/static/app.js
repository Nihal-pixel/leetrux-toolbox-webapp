function navigateTo(route) {
    window.location.href = window.origin + route
};

let e = ace.edit("editor");
e.getSession().setMode("ace/mode/python");
e.setTheme("ace/theme/terminal")

function getSelectedLanguage() {
    let selectedLanguage = document.getElementById("languages-dropdown-select").value;

    if (selectedLanguage == "Javascript") {
        e.getSession().setMode("ace/mode/javascript");
        e.setValue('console.log("Hello world!");');
    };

    if (selectedLanguage == "Python") {
        e.getSession().setMode("ace/mode/python");
        e.setValue('print("Hello world!")');
    };
};

function getSelectedTheme() {
    let selectedTheme = document.getElementById("theme-dropdown-select").value;

    if (selectedTheme == "xcode") {
        e.setTheme("ace/theme/xcode");
    } else if (selectedTheme == "Terminal") {
        e.setTheme("ace/theme/terminal");
    } else if (selectedTheme == "Github") {
        e.setTheme("ace/theme/github");
    } else if (selectedTheme == "Vibrant ink") {
        e.setTheme("ace/theme/vibrant_ink");
    } else if (selectedTheme == "Twilight") {
        e.setTheme("ace/theme/twilight");
    } else if (selectedTheme == "Tomorrow night") {
        e.setTheme("ace/theme/tomorrow_night");
    }
};

function getSelectedFontSize() {
    let selectedFontSize = document.getElementById("font-size-dropdown-select").value;

    if (selectedFontSize == "12") {
        document.getElementById('editor').style.fontSize='12px';
    } else if (selectedFontSize == "14") {
        document.getElementById('editor').style.fontSize='14px';
    } else if (selectedFontSize == "16") {
        document.getElementById('editor').style.fontSize='16px';
    } else if (selectedFontSize == "18") {
        document.getElementById('editor').style.fontSize='18px';
    } else if (selectedFontSize == "23") {
        document.getElementById('editor').style.fontSize='23px';
    } else if (selectedFontSize == "25") {
        document.getElementById('editor').style.fontSize='25px';
    } else if (selectedFontSize == "28") {
        document.getElementById('editor').style.fontSize='28px';
    } else if (selectedFontSize == "30") {
        document.getElementById('editor').style.fontSize='30px';
    } else if (selectedFontSize == "33") {
        document.getElementById('editor').style.fontSize='33px';
    } else if (selectedFontSize == "35") {
        document.getElementById('editor').style.fontSize='35px';
    } else if (selectedFontSize == "38") {
        document.getElementById('editor').style.fontSize='38px';
    } else if (selectedFontSize == "40") {
        document.getElementById('editor').style.fontSize='40px';
    };
};

function getSelectedIdentation() {
    let selectedIndentation = document.getElementById("identation-dropdown-select").value;

    if (selectedIndentation == "2") {
        e.session.setTabSize(2);
    } else if (selectedIndentation == "4") {
        e.session.setTabSize(4);
    } else if (selectedIndentation == "6") {
        e.session.setTabSize(6);
    } else if (selectedIndentation == "8") {
        e.session.setTabSize(8);
    } else if (selectedIndentation == "10") {
        e.session.setTabSize(10);
    } else if (selectedIndentation == "12") {
        e.session.setTabSize(12);
    } else if (selectedIndentation == "14") {
        e.session.setTabSize(14);
    };
};

// Simple example, see optional options for more configuration.
const pickr = Pickr.create({
    el: '.color-picker',
    theme: 'classic', // or 'monolith', or 'nano'

    swatches: [
        'rgba(244, 67, 54, 1)',
        'rgba(233, 30, 99, 0.95)',
        'rgba(156, 39, 176, 0.9)',
        'rgba(103, 58, 183, 0.85)',
        'rgba(63, 81, 181, 0.8)',
        'rgba(33, 150, 243, 0.75)',
        'rgba(3, 169, 244, 0.7)',
        'rgba(0, 188, 212, 0.7)',
        'rgba(0, 150, 136, 0.75)',
        'rgba(76, 175, 80, 0.8)',
        'rgba(139, 195, 74, 0.85)',
        'rgba(205, 220, 57, 0.9)',
        'rgba(255, 235, 59, 0.95)',
        'rgba(255, 193, 7, 1)'
    ],

    components: {

        // Main components
        preview: true,
        opacity: true,
        hue: true,

        // Input / output Options
        interaction: {
            hex: true,
            rgba: true,
            hsla: true,
            hsva: true,
            cmyk: true,
            input: true,
            clear: true,
            save: true
        }
    }
});

function deleteNoteFunction(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId })
    }).then(_res => {
        window.location.href = "/common-tools/notes"
    })
}


function getStackOverflowResults() {
    let errorValue = document.getElementById("search-focus").value;
    let links_div = document.getElementById("stack-overflow-links");
    // let API = "https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle=" + errorValue + "&site=stackoverflow";

    fetch("https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&q=" + errorValue + "&title=" + errorValue + "&site=stackoverflow").then(res => res.json()).then((data) => {
        console.log(data);
        links_div.innerHTML = ""
        for (let i = 0; i < data.items.length; i++) {
            let newA = document.createElement("a");
            let newBR = document.createElement("br");
            newA.href = data.items[i].link;
            newA.innerHTML = data.items[i].title;
            links_div.appendChild(newA);
            links_div.appendChild(newBR);
        }
    })
};