function delUser(idu, btn) {
    fetch('/admin/lock/user', {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "idu": idu,
            "lock": btn.value
        })
    }).then(res => res.json()).then(data => {

        if (data.status == 200) {

            btn.innerHTML = data.data + " Account";
            btn.value = data.data.toLowerCase();
            btn.parentElement.parentElement.parentElement.children[0].children[1].innerHTML = (data.data.toLowerCase() == "lock" ? "Active" : "InActive")

            alert((data.data.toLowerCase() == "lock" ? 'UnLock' : 'Lock') + " Success");
        }
    })
}

function get_stadium(home,away)
{
    fetch('/admin/match/get_stadium',{
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
        "hometeam": home,
        "awayteam": away
        })
    }).then(res => res.json()).then(data => {
            let dochtml = "<option value = '"+data.hometeam.id +"'>"+data.hometeam.stadium+" </option> <option value = '"+data.awayteam.id+"' > "+data.awayteam.stadium+"</option>"
            $("#stadium").removeAttr('disabled').empty().prepend(dochtml)
        })
}

function team_ready()
{
   let home= $("#hometeam").children("option:selected").val()
   let away = $("#awayteam").children("option:selected").val()
   if (home.length > 0 && away.length > 0 ) {
        if ( away !== home)
            get_stadium(home,away)
        else  $("#stadium").empty().prepend("<option value='' >Yêu cầu chọn hai đội khác nhau</option>").attr('disabled','')
   }
   else {
        $("#stadium").empty().prepend("<option value='' >Yêu cầu chọn đội</option>").attr('disabled','')

   }
}

function delmatch(idmatch) {
    let url = '/admin/match/delete'
    fetch(url, {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "idmatch": idmatch,
        })
    }).then(res => res.json()).then(data => {
        if (data.statuss == 400)
            alert("Xóa không thành công!!")
        else{

         location.reload()
        }


    })
}
function delgroup(idgroup) {
    let url = '/admin/group/delete'
    fetch(url, {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "idgroup": idgroup,
        })
    }).then(res => res.json()).then(data => {
        if (data.statuss == 400)
            alert("Xóa không thành công!!")
        else
           location.reload()
    })
}
function delround(idround) {
    let url = '/admin/round/delete'
    fetch(url, {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "idround": idround,
        })
    }).then(res => res.json()).then(data => {
        if (data.statuss == 400)
            alert("Xóa không thành công!!")
        else

           location.reload()
    })
}

