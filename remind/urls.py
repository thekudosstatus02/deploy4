<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="../../static/style.js"></script>
  <link rel="stylesheet" href="../../static/styles.css">
    <title>Document</title>
</head>
<body>
  hey, 
  {{ request.session.session_username }}
    {% if profile %}

      <h1>Profile</h1>
        name : {{profile.first_name|upper}}
        <br>
        mob no. : {{profile.phone_no}}
        <br>
        website : {{profile.website_name}}
        <br>
        about : {{profile.about}}
        <br>
        id : {{profile.id}}
        
        <form action="http://kudos02.pythonanywhere.com/edit-profile/" method="post">
            {% csrf_token %}
            <!-- {{form.data['user']} -->
            {{form.as_p}}
            <input type="submit" value="Edit">
        </form>

    {% else %} 
     
        <p> Edit Profile please...</p>
        <form action="http://kudos02.pythonanywhere.com/add-profile/?username={{username}}" method="post">
            {% csrf_token %}
            {{form.as_p}}
            <!-- <input type="submit" value="Edit"> -->
        </form>

    {% endif %}

    <a href="http://kudos02.pythonanywhere.com/logout"> Logout </a>
    <div class="footer">
        <div class="footer_dimensions">

          <a onclick="mySearch()" class="pluudo_mid_icons" id="search_icon">
            <img src="../static/anne/Pluudo_Search.png" alt="Pluudo_Search_icon">
          </a>
            <a class="pluudo_mid_icons" href="">
              <img src="../static/anne/Pluudo_Add_Video.png" alt="Pluudo_Search_icon">
            </a>
            {% if request.session.session_username %}
            <a class="pluudo_mid_icons" href="http://kudos02.pythonanywhere.com/view-profile">
              <img src="../static/anne/Pluudo_Profile.png" alt="Pluudo_Profile_icon">
            </a>
            {% else %}
            <a onclick="myProfile()" class="pluudo_mid_icons" >
              <img src="../static/anne/Pluudo_Profile.png" alt="Pluudo_Profile_icon">
            </a>
            {% endif %}

        </div>
        <div>
          <!-- <a class="back_icon" href="#">
            <img src="../static/anne/BACKBUTTON.png" alt="Pluudo_Home">
          </a> -->
          <a class="pluudo_icon" href="http://kudos02.pythonanywhere.com/">
            <img src="../static/anne/Pluudo_Home.png" alt="Pluudo_Home">
          </a>
        </div>
      </div>
</body>
</html>