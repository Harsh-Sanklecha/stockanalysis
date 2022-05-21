/* Loader */

$(window).on("load", function () {
    $(".loader-wrapper").fadeOut("slow");
});

/* Animate on Scroll */

AOS.init();
AOS.init({
    delay: 100,
    duration: 900,
    once: true,
    anchorPlacement: 'center-center',

});

/* Data Table */

$(document).ready(function () {
    $('#reportTable').DataTable({
    });
});


/* Accordion */

var acc = $('.accoridon');

for (var i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function () {
        var panel = this.nextElementSibling;

        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
        }
        else {
            panel.style.maxHeight = panel.scrollHeight + 'px';
        }
    })
}