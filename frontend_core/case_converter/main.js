function capitalize(text) {
    return text.substring(0, 1).toUpperCase() + text.substring(1).toLowerCase();
}

function download(filename, text) {
    let element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

let textarea = document.querySelector("textarea");
let upperCaseButton = document.getElementById("upper-case");
let lowerCaseButton = document.getElementById("lower-case");
let properCaseButton = document.getElementById("proper-case");
let sentenceCaseButton = document.getElementById("sentence-case");
let saveTextFile = document.getElementById("save-text-file");

upperCaseButton.addEventListener("click", () => {
    textarea.value = textarea.value.toUpperCase();
});

lowerCaseButton.addEventListener("click", () => {
    textarea.value = textarea.value.toLowerCase();
});

properCaseButton.addEventListener("click", () => {
    textarea.value = textarea.value.split(" ").map(s => capitalize(s)).join(" ");
});

sentenceCaseButton.addEventListener("click", () => {
    let text = textarea.value;
    textarea.value = text.split(".").map(s => capitalize(s.trim())).join(". ").trim();
});

saveTextFile.addEventListener("click", () => {
    download("text.txt", textarea.value);
})