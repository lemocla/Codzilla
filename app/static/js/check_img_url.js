$(document).ready(function () {
    // Variables
    let src;
    let checkUrl;
    let checkUrlValid;
    let checkVal;
    let checkArray;
    let errorMsg;

    // Check images format function
    function checkImgUrl(targetImg, formData, value) {
        if (!formData) {
            src = targetImg.attr("src");
        } else {
            src = targetImg.val();
        }
        //Check if url 
        checkUrl = ["https:", "http:"];
        checkUrlValid = [];
        //Check url valid 
        checkVal = ["svg", "png", "jpg", "jpeg", "tiff", "webp", "bmp", "heif"];
        checkArray = [];
        // check for url extension
        $.each(checkUrl, function (key, value) {
            checkUrlValid.push(src.includes(value));
        });
        // check for img extension 
        $.each(checkVal, function (key, value) {
            checkArray.push(src.includes(value));
        });
        // check image display on load
        if (!formData) {
            // Default image value if url invalid
            if (!checkUrlValid.includes(true)) {
                targetImg.attr("src", `/static/images/${value}_default.png`);
            } else {
                if (!checkArray.includes(true)) {
                    // Default image value if url valid but no image extension
                    targetImg.attr("src", `/static/images/${value}_default.png`);
                }
            }
        } else {
            // Display error on form imput 
            errorMsg = "Leave blank or include a valid image Url and make sure that it contains an image extension such as png, jpg...";
            // check starts with http or https
            if (!checkUrlValid.includes(true)) {
                $(`p[data-error=${targetImg.attr("id")}]`).html(errorMsg).removeClass("hide");
            } else {
                $(`p[data-error=${targetImg.attr("id")}]`).html(errorMsg).addClass("hide");
            }
            // Check for image extension
            if (!checkArray.includes(true)) {
                $(`p[data-error=${targetImg.attr("id")}]`).html(errorMsg).removeClass("hide");
            } else {
                $(`p[data-error=${targetImg.attr("id")}]`).html(errorMsg).addClass("hide");
            }
        }
    }

    // Default images for groups 
    $("img[data-default=group]").each(function () {
        checkImgUrl($(this), false, "group");
    });

    // Default images for events
    $("img[data-default=event]").each(function () {
        checkImgUrl($(this), false, "event");
    });

    // Default images for avatars
    $("img[data-default=avatar]").each(function () {
        checkImgUrl($(this), false, "avatar");
    });

    //Check imgage url in forms 
    $("textarea[data-input=img]").change(function () {
        if ($(this).val() != "") {
            checkImgUrl($(this), true, "");
        } else {
            $(`p[data-error=${$(this).attr("id")}]`).addClass("hide");
        }
    });
});