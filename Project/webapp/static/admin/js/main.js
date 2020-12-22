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

function get_stadium(home) {
    fetch('/admin/match/get_stadium', {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "hometeam": home
        })
    }).then(res => res.json()).then(data => {
        let dochtml = "<option>" + data.hometeam.stadium + " </option>"
        $("#stadium").empty().prepend(dochtml)
    })
}

function team_ready() {
    let home = $("#hometeam").children("option:selected").val()
    if (home.length > 0) {
        get_stadium(home)
    } else {
        $("#stadium").empty().prepend("<option value='' >Yêu cầu chọn đội nhà</option>").attr('disabled', '')
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
        else {

            location.reload()
        }
    })
}

function getmatch(idmatch) {
    let url = '/admin/match/list/'
    fetch(url, {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "idmatch": idmatch,
        })
    }).then(res => res.json()).then(data => {
        if (data.statuss == 400)
            alert("Thêm kết quả cho trận đấu")
        else {
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

function sent_account(idt) {
    fetch('/admin/accounts?action=sent_account', {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "idt": idt,

        })
    }).then(res => res.json()).then(data => {
        alert((data.status == 200 ? "Success" : "Error") + ' Sent Account')
    })
}

function delplayer(playerid, btn) {
    var nameplayer = btn.parentElement.parentElement.children[1].innerText
    var r = confirm('Bạn chắc chắn xóa cầu thủ "' + nameplayer + '"')

    if (r == true) {
        fetch('/user/players?action=delete', {
            method: 'POST',
            headers: {"Content-Type": 'application/json'},
            body: JSON.stringify({
                "playerid": playerid,

            })
        }).then(res => res.json()).then(data => {
            alert((data.data == true ? "Success" : "Error") + ' delete player')
            location.reload()
        })
    }

}

$('#exampleModal').on('show.bs.modal', function (event) {
    var row = $(event.relatedTarget) // Button that triggered the modal
    var modal = $(this)
    fetch('/user/players?action=GET', {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "playerid": row.data('id'),
        })
    }).then(res => res.json()).then(data => {
        if (data.data != "error") {
            console.log(data)
            modal.find('.modal-title').text('Edit ' + data.firstname + " " + data.lastname)
            $("#lastname").val(data.lastname)
            $("#firstname").val(data.firstname)
            $("#birthdate").val(data.birthdate)
            $("#gender").val(data.gender)
            $("#typeplayer").val(data.typeplayer)
            $("#nationality").val(data.nationality)
            $("#position").val(data.position)
            $("#number").val(data.number)
            $("#playerid").val(row.data("id"))

        }
    })
})

function validateFileType() {
    var fileName = document.getElementById("avatar").value;
    var idxDot = fileName.lastIndexOf(".") + 1;
    var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
    if (extFile == "jpg" || extFile == "jpeg" || extFile == "png") {
        //TO DO
    } else {
        alert("file không đúng định dạng vui lòng chọn lại");
        fileName.value = null
    }
}

//sort nationality
$("#nationality").click(function () {
    var my_options = $("#nationality option");
    my_options.sort(function (a, b) {
        if (a.text > b.text) return 1;
        else if (a.text < b.text) return -1;
        else return 0;
    });

    $("#nationality").empty().append(my_options);
});
// write result
$('#writeresult').on('show.bs.modal', function (event) {
    var row = $(event.relatedTarget) // Button that triggered the modal
    var modal = $(this)
    test = null
    //set title
    modal.find('.modal-title').text(row.data("match"))
    modal.find('#awayname').text(row.data("awayname"))
    modal.find('#homename').text(row.data("homename"))
    $("#homegoalplayer tbody tr:not('tr#row_goalhome')").remove()
    $("#awaygoalplayer tbody tr:not('tr#row_goalaway')").remove()
    fetch('/admin/results?action=GET', {
        method: 'POST',
        headers: {"Content-Type": 'application/json'},
        body: JSON.stringify({
            "matchid": row.data('matchid'),
            "hometeamid": row.data('hometeam'),
            "awayteamid": row.data('awayteam')
        })
    }).then(res => res.json()).then(data => {

        if (data.data != "error") {
            $("#row_goalhome select.homeplayers").empty().append(["<option selected value='' disabled>Chọn cầu thủ</option>", data.data.home.player])
            $("#row_goalaway select.awayplayers").empty().append(["<option selected value='' disabled>Chọn cầu thủ</option>", data.data.away.player])
            console.log(data.data)
            var tableresulthome = $("#homegoalplayer tbody")
            var tableresultaway = $("#awaygoalplayer tbody")
            var resulthome = data.data.home.result
            for (i = 0; i < resulthome.length; i++) {
                var row = $("#row_goalhome").clone()
                row.find('select.homeplayers').val(resulthome[i].playerid)
                row.find('select.hometypegoal').val(resulthome[i].type)
                row.find('select.hometime').val(resulthome[i].time)
                row.removeAttr('id').css('display', '')
                tableresulthome.append(row)
                console.log(row[0])

            }
            var resultaway = data.data.away.result
            for (i = 0; i < resultaway.length; i++) {
                var row = $("#row_goalaway").clone()
                row.find('select.awayplayers').val(resultaway[i].playerid)
                row.find('select.awaytypegoal').val(resultaway[i].type)
                row.find('select.awaytime').val(resultaway[i].time)
                row.removeAttr('id').css('display', '')
                tableresultaway.append(row)
                console.log(resultaway[i].playerid)
            }


        }
    })
})


function addgoal(btn) {
    if (btn == "home") {
        var inputamountgoal = $("#amountgoalhome")
        inputamountgoal.val(parseInt(inputamountgoal.val()) + 1)
        var table = $("#homegoalplayer tbody")
        var row = $("#row_goalhome").clone()
        row.removeAttr('id').css('display', '')
        $(table).append(row)
    }
    if (btn == "away") {
        var inputamountgoal = $("#amountgoalaway")
        inputamountgoal.val(parseInt(inputamountgoal.val()) + 1)
        var table = $("#awaygoalplayer tbody")
        var row = $("#row_goalaway").clone()
        row.removeAttr('id').css('display', '')
        $(table).append(row)
    }

}
