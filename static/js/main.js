$('.dropdown-item').click(function(){
    $("#team-info").css("display", "none");
    var itemText = this.text;
    $("#team-info").html("<h2>"+itemText+"</h2>");
    $("#team-info").fadeIn();
})