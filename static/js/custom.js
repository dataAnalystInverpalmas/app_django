$(document).ready(function() {
    $("#id_group").change(function () {
        const url = $("#recordForm").data("ajax-load-sub-groups");
        const groupId = $(this).val();
        console.log(groupId );
        $.get(url, { group_id: groupId }, function (data) {
            $("#id_sub_group").html(data);
        });
    });
});
