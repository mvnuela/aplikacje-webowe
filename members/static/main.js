Dropzone.autoDiscover = false;
const myDropzone = new Dropzone("#my-dropzone", {
    url: "usersolution/",
    maxFiles : 1,
    acceptedFiles: ".png, .jpg"
})