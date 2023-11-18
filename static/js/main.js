(function () {
    "use strict";

    var treeviewMenu = $(".app-menu");

    // Toggle Sidebar
    $('[data-toggle="sidebar"]').click(function (event) {
        event.preventDefault();
        $(".app").toggleClass("sidenav-toggled");
        localStorage.setItem('collapsed', $(".app").hasClass('sidenav-toggled'));
    });

    // Activate sidebar treeview toggle
    $("[data-toggle='treeview']").click(function (event) {
        event.preventDefault();
        if (
            !$(this)
                .parent()
                .hasClass("is-expanded")
        ) {
            treeviewMenu
                .find("[data-toggle='treeview']")
                .parent()
                .removeClass("is-expanded");
        }
        $(this)
            .parent()
            .toggleClass("is-expanded");
    });

    // Set initial active toggle
    $("[data-toggle='treeview.'].is-expanded")
        .parent()
        .toggleClass("is-expanded");

    //Activate bootstrip tooltips
    $("[data-toggle='tooltip']").tooltip();

    //show any notifications
    $("input.meta-messages").each(function () {
        var result = $(this);
        if (result.val()) {
            var result_type = null;
            switch (result.data("level")) {
                case 20:
                    result_type = "info";
                    break;
                case 25:
                    result_type = "success";
                    break;
                case 40:
                    result_type = "danger";
            }
            $.notify(
                {
                    message: result.val(),
                    icon: result_type == "danger" ? "fa fa-times" : "fa fa-check"
                },
                {
                    type: result_type
                }
            );
        }
    });

    if (JSON.parse(localStorage.getItem('collapsed'))) {
        $(".app").addClass('sidenav-toggled');
    }

    $(".date-picker").datetimepicker({
        timepicker: false,
        format: 'Y-m-d'
    });

    $(".time-picker").datetimepicker({
        datepicker: false,
        format: 'H:i'
    });
})();
