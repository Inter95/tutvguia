# coding: utf-8
__author__ = 'Ruben'
import requests

data = '''

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <!---->
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-script-type" content="text/javascript" />
<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" />
<meta http-equiv='cache-control' content='no-cache' />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<title>Alt-Torrent - Calidad</title>
<meta name="description" content="Alt-torrent Películas con audio latino para ver y compartir" />
<meta name="keywords" content="Alt-torrent, audio latino, torrent, estrenos, movie, peliculas, series" />
<meta name="robots" content="INDEX,FOLLOW" />
<link rel="icon" href="/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
<!--<meta name="propeller" content="79061afba9c3428d8ef98194e97b8a42">-->
<!--[if lt IE 7]>
<script type="text/javascript">
//<![CDATA[
    var BLANK_URL = '/js/blank.html';
    var BLANK_IMG = '/js/spacer.gif';
//]]>
</script>
<![endif]-->

<!--[if lt IE 8]>
<link rel="stylesheet" type="text/css" href="/themes/audiolatino/css/styles-ie.css" media="all" />
<![endif]-->
<!--[if IE 7]>
<script type="text/javascript" src="/themes/audiolatino/js/ds-sleight.js"></script>
<script src="http://ie7-js.googlecode.com/svn/version/2.1(beta4)/IE7.js"></script>
<link rel="stylesheet" type="text/css" href="/themes/audiolatino/css/styles-ie.css" media="all" />
  <link rel="stylesheet" href="/lib/css/font-awesome-ie7.css" media="all">
<![endif]-->
<!--<script type="text/javascript" src="/lib/js/jquery.js"></script>-->
<!--<script type="text/javascript" src="/lib/js/raty.js"></script>-->
<!--<script type="text/javascript" src="/lib/js/flexslider.js"></script>-->
<link href="../lib/css/bootstrap.css" rel="stylesheet" type="text/css"/>
<link href="../lib/css/bootstrap-theme.css" rel="stylesheet" type="text/css"/>

<!--<link href="../lib/css/navbar.css" rel="stylesheet" type="text/css"/>-->
  </head>
  <body>
    <header class="navbar navbar-inverse navbar-fixed-top" role="navigation">
  <div class="container">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <a class="navbar-brand" href="/"><i class="icon-home"></i></a>
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
    </div>


    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse navbar-ex1-collapse">

      <ul class="nav navbar-nav">
        <li><a href="/sinaudiolatino.html">Otro Idioma</a></li>
                            <li class="dropdown">
                              <a data-toggle="dropdown" class="dropdown-toggle" href="/">Genero <b class="caret"></b></a>
                <ul class="dropdown-menu">
                                        <li><a href="/catalogo/genero/accion.html">Acción</a></li>
                                            <li><a href="/catalogo/genero/animacion.html">Animación</a></li>
                                            <li><a href="/catalogo/genero/aventura.html">Aventura</a></li>
                                            <li><a href="/catalogo/genero/ciencia-ficcion.html">Ciencia ficción</a></li>
                                            <li><a href="/catalogo/genero/comedia.html">Comedia</a></li>
                                            <li><a href="/catalogo/genero/crimen.html">Crimen</a></li>
                                            <li><a href="/catalogo/genero/documental.html">Documental</a></li>
                                            <li><a href="/catalogo/genero/drama.html">Drama</a></li>
                                            <li><a href="/catalogo/genero/familia.html">Familia</a></li>
                                            <li><a href="/catalogo/genero/fantasa.html">Fantasía</a></li>
                                            <li><a href="/catalogo/genero/guerra.html">Guerra</a></li>
                                            <li><a href="/catalogo/genero/historia.html">Historia</a></li>
                                            <li><a href="/catalogo/genero/romance.html">Romance</a></li>
                                            <li><a href="/catalogo/genero/terror.html">Terror</a></li>
                                            <li><a href="/catalogo/genero/western.html">Western</a></li>
                                      </ul>
                          </li>
                      <li class="dropdown">
                              <a data-toggle="dropdown" class="dropdown-toggle" href="/">Calidad <b class="caret"></b></a>
                <ul class="dropdown-menu">
                                        <li><a href="/catalogo/calidad/1080p.html">1080p</a></li>
                                            <li><a href="/catalogo/calidad/3d.html">3D</a></li>
                                            <li><a href="/catalogo/calidad/720p.html">720p</a></li>
                                            <li><a href="/catalogo/calidad/bluray.html">BLURAY</a></li>
                                            <li><a href="/catalogo/calidad/fullhd.html">FullHD</a></li>
                                            <li><a href="/catalogo/calidad/webdl-1080p.html">WEBDL-1080p</a></li>
                                      </ul>
                          </li>

        <li class="dropdown">
          <a data-toggle="dropdown" class="dropdown-toggle" href="/">Año<b class="caret"></b></a>
          <ul class="dropdown-menu">
                              <li class="dropdown-submenu"> <a href="#">2010</a>
                    <ul class="dropdown-menu">
                                          <li><a href="/catalogo/year/2015.html">2015</a></li>
                                      <li><a href="/catalogo/year/2014.html">2014</a></li>
                                      <li><a href="/catalogo/year/2013.html">2013</a></li>
                                      <li><a href="/catalogo/year/2012.html">2012</a></li>
                                      <li><a href="/catalogo/year/2011.html">2011</a></li>
                                      <li><a href="/catalogo/year/2010.html">2010</a></li>
                  </ul></li>                  <li class="dropdown-submenu"> <a href="#">2000</a>
                    <ul class="dropdown-menu">
                                          <li><a href="/catalogo/year/2009.html">2009</a></li>
                                      <li><a href="/catalogo/year/2008.html">2008</a></li>
                                      <li><a href="/catalogo/year/2007.html">2007</a></li>
                                      <li><a href="/catalogo/year/2006.html">2006</a></li>
                                      <li><a href="/catalogo/year/2005.html">2005</a></li>
                                      <li><a href="/catalogo/year/2004.html">2004</a></li>
                                      <li><a href="/catalogo/year/2003.html">2003</a></li>
                                      <li><a href="/catalogo/year/2002.html">2002</a></li>
                                      <li><a href="/catalogo/year/2001.html">2001</a></li>
                                      <li><a href="/catalogo/year/2000.html">2000</a></li>
                  </ul></li>                  <li class="dropdown-submenu"> <a href="#">1990</a>
                    <ul class="dropdown-menu">
                                          <li><a href="/catalogo/year/1999.html">1999</a></li>
                                      <li><a href="/catalogo/year/1998.html">1998</a></li>
                                      <li><a href="/catalogo/year/1997.html">1997</a></li>
                                      <li><a href="/catalogo/year/1996.html">1996</a></li>
                                      <li><a href="/catalogo/year/1995.html">1995</a></li>
                                      <li><a href="/catalogo/year/1994.html">1994</a></li>
                                      <li><a href="/catalogo/year/1993.html">1993</a></li>
                                      <li><a href="/catalogo/year/1992.html">1992</a></li>
                                      <li><a href="/catalogo/year/1991.html">1991</a></li>
                                      <li><a href="/catalogo/year/1990.html">1990</a></li>
                  </ul></li>                  <li class="dropdown-submenu"> <a href="#">1980</a>
                    <ul class="dropdown-menu">
                                          <li><a href="/catalogo/year/1989.html">1989</a></li>
                                      <li><a href="/catalogo/year/1988.html">1988</a></li>
                                      <li><a href="/catalogo/year/1987.html">1987</a></li>
                                      <li><a href="/catalogo/year/1986.html">1986</a></li>
                                      <li><a href="/catalogo/year/1985.html">1985</a></li>
                                      <li><a href="/catalogo/year/1984.html">1984</a></li>
                                      <li><a href="/catalogo/year/1983.html">1983</a></li>
                                      <li><a href="/catalogo/year/1982.html">1982</a></li>
                                      <li><a href="/catalogo/year/1981.html">1981</a></li>
                                      <li><a href="/catalogo/year/1980.html">1980</a></li>
                  </ul></li>                  <li class="dropdown-submenu"> <a href="#">1970</a>
                    <ul class="dropdown-menu">
                                          <li><a href="/catalogo/year/1979.html">1979</a></li>
                                      <li><a href="/catalogo/year/1978.html">1978</a></li>
                                      <li><a href="/catalogo/year/1977.html">1977</a></li>
                                      <li><a href="/catalogo/year/1976.html">1976</a></li>
                                      <li><a href="/catalogo/year/1975.html">1975</a></li>
                                      <li><a href="/catalogo/year/1974.html">1974</a></li>
                                      <li><a href="/catalogo/year/1973.html">1973</a></li>
                                      <li><a href="/catalogo/year/1972.html">1972</a></li>
                                      <li><a href="/catalogo/year/1971.html">1971</a></li>
                                      <li><a href="/catalogo/year/1970.html">1970</a></li>
                  </ul></li>                  <li class="dropdown-submenu"> <a href="#">1960</a>
                    <ul class="dropdown-menu">
                                          <li><a href="/catalogo/year/1969.html">1969</a></li>
                                      <li><a href="/catalogo/year/1968.html">1968</a></li>
                                      <li><a href="/catalogo/year/1967.html">1967</a></li>
                                      <li><a href="/catalogo/year/1966.html">1966</a></li>
                                      <li><a href="/catalogo/year/1965.html">1965</a></li>
                                      <li><a href="/catalogo/year/1964.html">1964</a></li>
                                      <li><a href="/catalogo/year/1963.html">1963</a></li>
                                      <li><a href="/catalogo/year/1962.html">1962</a></li>
                                      <li><a href="/catalogo/year/1961.html">1961</a></li>
                                      <li><a href="/catalogo/year/1960.html">1960</a></li>
                  </ul></li>                  <li class="dropdown-submenu"> <a href="#">1950</a>
                    <ul class="dropdown-menu">
                                          <li><a href="/catalogo/year/1959.html">1959</a></li>
                                      <li><a href="/catalogo/year/1958.html">1958</a></li>
                                      <li><a href="/catalogo/year/1956.html">1956</a></li>
                                      <li><a href="/catalogo/year/1955.html">1955</a></li>
                                      <li><a href="/catalogo/year/1953.html">1953</a></li>
                                      <li><a href="/catalogo/year/1951.html">1951</a></li>
                                      <li><a href="/catalogo/year/1950.html">1950</a></li>
                  </ul></li>                  <li class="dropdown-submenu"> <a href="#">1940</a>
                    <ul class="dropdown-menu">
                                          <li><a href="/catalogo/year/1942.html">1942</a></li>
                                      <li><a href="/catalogo/year/1941.html">1941</a></li>
                                      <li><a href="/catalogo/year/1940.html">1940</a></li>
                  </ul></li>                  <li class="dropdown-submenu"> <a href="#">1930</a>
                    <ul class="dropdown-menu">
                                          <li><a href="/catalogo/year/1939.html">1939</a></li>
                                      <li><a href="/catalogo/year/1933.html">1933</a></li>
                                </ul>
            </li>
          </ul>
        </li>
        <li><a href="/series.html">Series</a></li>
        <li>
                        <a href="/pedidos.html">Pedidos</a>
            </li>
      </ul>

      <ul class="nav navbar-nav pull-right" >
        <li>
          <a title="Facebook" target="_blank"class="btn btn_circle icon-facebook" href="http://www.facebook.com/pages/Audiolatino-torrent/129387667222488" >&nbsp;</a>
          <a title="Twitter" target="_blank" class="btn btn_circle icon-twitter" href="https://twitter.com/AudiolatinoT"  > </a>
          <a title="Google+" target="_blank"class="btn btn_circle icon-google-plus" href="https://plus.google.com/u/0/communities/117551418133781957396"  >&nbsp;</a>
          <a title="Pinterest" target="_blank" class="btn btn_circle icon-pinterest" href="http://www.pinterest.com/audiolatinot">&nbsp;</a>
          <!--<a title="Facebook" target="_blank"class="btn btn_circle icon-facebook" href="http://www.facebook.com/sharer.php?u=http://" >&nbsp;</a>-->
          <!--<a title="In" class="btn btn_follow btn_follow_Googplus" href="#">&nbsp;</a>-->
        </li>
      </ul>

      <ul class="nav navbar-nav" >
                    <li class="dropdown">
              <a data-toggle="dropdown" class="dropdown-toggle" href="#"><i class="icon-user"></i> mancuniancol <b class="caret"></b></a>
              <ul class="dropdown-menu">
                <!--                <li><a href="/cuenta/">Mis Datos</a></li>
                                <li><a href="/cuenta/">Mis compras</a></li>-->
                <li><a href="/ajax/logout.html" >Cerrar sesión</a></li>
              </ul>
            </li>
                </ul>
    </div><!-- /.navbar-collapse -->

  </div>
</header>

<!-- LOGIN -->
<div class="modal modal-static fade" id="Login" role="dialog" aria-hidden="true">
  <div class="col-xs-12 col-sm-6 col-sm-offset-3 col-lg-4 col-lg-offset-4 modal-border" >
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">x</button>
        <h3>Login</h3>
      </div>
      <div class="modal-body">
        <form method="post" action='' name="login_form"  id="login_form" accept-charset="UTF-8" role="form">
          <fieldset>
            <div class="form-group">
              <div class="input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-user"></i></span>
                <input class="form-control" placeholder="Usuario" name="user" id="user" type="text">
              </div>
            </div>
            <div class="form-group">
              <div class="input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-lock"></i></span>
                <input class="form-control" placeholder="Password" name="password" type="password" value="">
              </div>
            </div>
            <!--            <div class="checkbox">
                          <label>
                            <input name="remember" type="checkbox" value="Remember Me"> Remember Me
                          </label>
                        </div>-->
            <input class="btn btn-lg btn-primary btn-block" type="submit" value="Login">
          </fieldset>
        </form>
      </div>
      <div class="modal-footer">
        <div class="form-group">
          <a onclick="forgot();">Olvidaste clave?</a>
        </div>
        <a onclick="signup();" class="btn btn-success" data-toggle="modal">Soy nuevo</a>
      </div>
    </div>
  </div>

</div> <!-- LOGIN -->


<!-- SIGNUP -->
<div class="modal modal-static fade" id="Signup" role="dialog" aria-hidden="true">
  <div class="col-xs-12 col-sm-6 col-sm-offset-3 col-lg-4 col-lg-offset-4 modal-border" >
    <div class="modal-content">
      <div class="modal-body">
        <button type="button" class="close" data-dismiss="modal">x</button>
        <legend><a href="http://www.alt-torrent.com"><i class="glyphicon glyphicon-globe"></i></a> Sign up!</legend>
        <form method="post" action='/ajax/signup.html' name="signup_form"  id="signup_form" accept-charset="UTF-8" role="form">
          <fieldset>
            <div class="form-group">
              <div class="input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-user"></i></span>
                <input class="form-control" placeholder="Usuario" name="s_username" id="s_username"type="text">
              </div>
            </div>
            <div class="form-group">
              <div class="input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-envelope"></i></span>
                <input class="form-control" placeholder="E-mail" name="s_email" id="s_email"type="text">
              </div>
            </div>
            <div class="form-group">
              <div class="input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-lock"></i></span>
                <input class="form-control" placeholder="Password" name="s_password" id="s_password" type="password" >
              </div>
            </div>
            <div class="form-group">
              <div class="input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-lock"></i></span>
                <input class="form-control" placeholder="Repite Password" name="s_password2" id="s_password2" type="password" >
              </div>
            </div>

            <label for="">Fecha de nacimiento</label>
            <div class="row">
              <div class="col-xs-4 col-md-4 form-group">
                <select class="form-control" name="dia">
                  <option value="">Día</option>
                                        <option value="1" >01</option>
                                          <option value="2" >02</option>
                                          <option value="3" >03</option>
                                          <option value="4" >04</option>
                                          <option value="5" >05</option>
                                          <option value="6" >06</option>
                                          <option value="7" >07</option>
                                          <option value="8" >08</option>
                                          <option value="9" >09</option>
                                          <option value="10" >10</option>
                                          <option value="11" >11</option>
                                          <option value="12" >12</option>
                                          <option value="13" >13</option>
                                          <option value="14" >14</option>
                                          <option value="15" >15</option>
                                          <option value="16" >16</option>
                                          <option value="17" >17</option>
                                          <option value="18" >18</option>
                                          <option value="19" >19</option>
                                          <option value="20" >20</option>
                                          <option value="21" >21</option>
                                          <option value="22" >22</option>
                                          <option value="23" >23</option>
                                          <option value="24" >24</option>
                                          <option value="25" >25</option>
                                          <option value="26" >26</option>
                                          <option value="27" >27</option>
                                          <option value="28" >28</option>
                                          <option value="29" >29</option>
                                          <option value="30" >30</option>
                                          <option value="31" >31</option>
                                    </select>
              </div>
              <div class="col-xs-4 col-md-4 form-group">
                <select class="form-control" name="mes">
                  <option value="">Mes</option>
                                        <option value="1" >01</option>
                                          <option value="2" >02</option>
                                          <option value="3" >03</option>
                                          <option value="4" >04</option>
                                          <option value="5" >05</option>
                                          <option value="6" >06</option>
                                          <option value="7" >07</option>
                                          <option value="8" >08</option>
                                          <option value="9" >09</option>
                                          <option value="10" >10</option>
                                          <option value="11" >11</option>
                                          <option value="12" >12</option>
                                    </select>
              </div>
              <div class="col-xs-4 col-md-4 form-group">
                <select class="form-control" name="ano">
                  <option value="">Año</option>
                                        <option value="2015" >2015</option>
                                          <option value="2014" >2014</option>
                                          <option value="2013" >2013</option>
                                          <option value="2012" >2012</option>
                                          <option value="2011" >2011</option>
                                          <option value="2010" >2010</option>
                                          <option value="2009" >2009</option>
                                          <option value="2008" >2008</option>
                                          <option value="2007" >2007</option>
                                          <option value="2006" >2006</option>
                                          <option value="2005" >2005</option>
                                          <option value="2004" >2004</option>
                                          <option value="2003" >2003</option>
                                          <option value="2002" >2002</option>
                                          <option value="2001" >2001</option>
                                          <option value="2000" >2000</option>
                                          <option value="1999" >1999</option>
                                          <option value="1998" >1998</option>
                                          <option value="1997" >1997</option>
                                          <option value="1996" >1996</option>
                                          <option value="1995" >1995</option>
                                          <option value="1994" >1994</option>
                                          <option value="1993" >1993</option>
                                          <option value="1992" >1992</option>
                                          <option value="1991" >1991</option>
                                          <option value="1990" >1990</option>
                                          <option value="1989" >1989</option>
                                          <option value="1988" >1988</option>
                                          <option value="1987" >1987</option>
                                          <option value="1986" >1986</option>
                                          <option value="1985" >1985</option>
                                          <option value="1984" >1984</option>
                                          <option value="1983" >1983</option>
                                          <option value="1982" >1982</option>
                                          <option value="1981" >1981</option>
                                          <option value="1980" >1980</option>
                                          <option value="1979" >1979</option>
                                          <option value="1978" >1978</option>
                                          <option value="1977" >1977</option>
                                          <option value="1976" >1976</option>
                                          <option value="1975" >1975</option>
                                          <option value="1974" >1974</option>
                                          <option value="1973" >1973</option>
                                          <option value="1972" >1972</option>
                                          <option value="1971" >1971</option>
                                          <option value="1970" >1970</option>
                                          <option value="1969" >1969</option>
                                          <option value="1968" >1968</option>
                                          <option value="1967" >1967</option>
                                          <option value="1966" >1966</option>
                                          <option value="1965" >1965</option>
                                          <option value="1964" >1964</option>
                                          <option value="1963" >1963</option>
                                          <option value="1962" >1962</option>
                                          <option value="1961" >1961</option>
                                          <option value="1960" >1960</option>
                                          <option value="1959" >1959</option>
                                          <option value="1958" >1958</option>
                                          <option value="1957" >1957</option>
                                          <option value="1956" >1956</option>
                                          <option value="1955" >1955</option>
                                          <option value="1954" >1954</option>
                                          <option value="1953" >1953</option>
                                          <option value="1952" >1952</option>
                                          <option value="1951" >1951</option>
                                          <option value="1950" >1950</option>
                                    </select>
              </div>
            </div>

            <div class="row">
              <div class="col-xs-12 form-group">
                <select class="form-control" name="gender">
                  <option value="">Selecciona sexo</option>
                  <option value="H">Hombre</option>
                  <option value="M">Mujer</option>
                </select>
              </div>

            </div>
            <br />
            <div class="row">
              <div class="col-xs-3 col-sm-3 col-md-3">
                <span class="button-checkbox">
                  <button type="button" class="btn" data-color="info" tabindex="7">Acepto</button>
                  <input type="checkbox" name="terminos" id="terminos" class="hidden" value="1">
                </span>
              </div>
              <div class="col-xs-9 col-sm-9 col-md-9">
                Estoy de acuerdo con los
                <a href="#" data-toggle="modal" data-target="#t_and_c_m">Términos y Condiciones</a>
                establecidos por este sitio, incluyendo nuestro uso de cookies.
              </div>
            </div>
            <br />
            <div class="row">
              <input id="submit_signup"class="btn btn-lg btn-primary btn-block" type="submit" value="Registrarme" >
            </div>
          </fieldset>
        </form>
      </div>
    </div>
  </div>

</div><!-- SIGNUP -->

<!-- CHANGEPASS -->
<div class="modal modal-static fade" id="Forgot" role="dialog" aria-hidden="true">
  <div class="col-xs-12 col-sm-6 col-sm-offset-3 col-lg-4 col-lg-offset-4 modal-border" >
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">x</button>
        <h3>Cambiar Contraseña</h3>
      </div>
      <div class="modal-body">
        <form method="post" action='' name="forgotForm"  id="forgotForm" accept-charset="UTF-8" role="form">
          <fieldset>
            <div class="form-group">
              <div class="input-group">
                <span  class="help-block ">Codigo verificación</span>
              </div>
              <div class="input-group">
                <span class="input-group-addon"><i class="icon-key"></i></span>
                <input class="form-control" placeholder="Codigo verificación" name="codigover" id="codigover" type="text" value="">
              </div>
            </div>
            <div class="form-group">
              <div class="input-group">
                <span  class="help-block">Nueva Contraseña</span>
              </div>
              <div class="input-group">
                <span class="input-group-addon"><i class="icon-lock"></i></span>
                <input class="form-control" name="f_newpass1" id="f_newpass1" type="password" >
              </div>
            </div>
            <div class="form-group">
              <div class="input-group">
                <span  class="help-block">Repite contraseña</span>
              </div>
              <div class="input-group">
                <span class="input-group-addon"><i class="icon-lock"></i></span>
                <input class="form-control" name="f_newpass2" id="f_newpass2" type="password" >
              </div>
            </div>
            <input class="btn btn-lg btn-primary btn-block" type="buton" onclick="forgotSubmit();" value="Cambiar">
          </fieldset>
        </form>
      </div>
      <div class="modal-footer">
        <div class="form-group">
          <a onclick="sendcode();" data-toggle="modal"><i class="icon-key"></i> Pedir código de verificación</a>
        </div>
      </div>
    </div>
  </div>

</div> <!-- CHANGEPASS -->


<!-- FORGOT -->
<div class="modal modal-static fade" id="SendCode" role="dialog" aria-hidden="true">
  <div class="col-xs-12 col-sm-6 col-sm-offset-3 col-lg-4 col-lg-offset-4 modal-border" >
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">x</button>
        <h3>Ingresa tu E-Mail</h3>
      </div>
      <div class="modal-body">
        <form method="post" action='' name="sendcodeForm"  id="sendcodeForm" accept-charset="UTF-8" role="form">
          <fieldset>
            <div class="form-group">
              <div class="input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-envelope"></i></span>
                <input class="form-control" placeholder="E-Mail" name="email" id="email" type="text">
              </div>
            </div>
            <input class="btn btn-lg btn-primary btn-block" type="buton" onclick="sendcodeSubmit();" value="Enviar Código" >
          </fieldset>
        </form>
      </div>

    </div>
  </div>

</div> <!-- FORGOT -->

<!-- SIGNUP-SUCCESS -->
<div class="modal modal-static fade" id="Signup-succes" role="dialog" aria-hidden="true">
  <div class="col-xs-12 col-sm-6 col-sm-offset-3 col-lg-4 col-lg-offset-4 modal-border" >
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">x</button>
        <h3>Registro existoso</h3>
      </div>
      <div class="modal-body">
        <h4>Gracias <span id="namelogin"></span> por registrarte con nosotros</h4>
        <p>Ahora puedes ingresar a buscar tus peliculas preferidas y comienzar a descargarlas.<br><br> No se te olvide compartir!!</p>

      </div>
      <div class="modal-footer">

        <a href="/" class="btn btn-default" >Aceptar</a>
      </div>
    </div>
  </div>

</div> <!-- SIGNUP-SUCCESS -->

    <div class="container boxed">
      <div id="screensize" class="navbar-fixed-top">
</div>
<div class="row">
  <div class="col-sm-4 col-lg-4">
    <a href="/">
      <img src="/images/logo.png" class="img-responsive" alt="Alt-Torrent" title="Audio Latino Torrent"/>
    </a>
  </div>
  <div class="col-xs-12 col-sm-12 col-md-6 col-lg-6 pull-right" style="z-index:1020 !important">
    <form method="get" action="/" class="navbar-form navbar-right" id="search_mini_form" role="search">
      <div class="form-group">
        <input type="text" class="form-control" placeholder="Nombre o cód IMDB" name="q" id="search" autocomplete="off" level-top="" parent="" />
      </div>
      <button type="submit" class="btn btn-default">Buscar</button>
      <div class="search-autocomplete" id="search_autocomplete" style="display: none;"></div>
      <script type="text/javascript">
        //<![CDATA[
        //        var searchForm = new Varien.searchForm('search_mini_form', 'search', 'Busqueda');
        //        searchForm.initAutocomplete('/ajax/sugiere.php/', 'search_autocomplete');
        //]]>
      </script>
    </form>
  </div><!-- Mini Cart -->
</div>

<!--<script language="javascript" type="text/javascript">
  jQuery(".shopping_bg").hover(function() {
    jQuery('.slideTogglebox').slideToggle(10);
  });
</script>-->      <div class="row">
        <!-- Sidebar -->
        <div class="visible-md visible-lg col-md-3 col-lg-3">

              <div class="list-group panel panel-primary">
                <div class="panel-heading list-group-item text-center hidden-xs">
                  <h4>Calidad</h4>
                </div>
                <div id="cat-navi">
                                      <a class="list-group-item hidden-xs "
                       href="/catalogo/calidad/1080p.html">
                      1080p</a>
                                      <a class="list-group-item hidden-xs active"
                       href="/catalogo/calidad/3d.html">
                      3D</a>
                                      <a class="list-group-item hidden-xs "
                       href="/catalogo/calidad/720p.html">
                      720p</a>
                                      <a class="list-group-item hidden-xs "
                       href="/catalogo/calidad/bluray.html">
                      BLURAY</a>
                                      <a class="list-group-item hidden-xs "
                       href="/catalogo/calidad/fullhd.html">
                      FullHD</a>
                                      <a class="list-group-item hidden-xs "
                       href="/catalogo/calidad/webdl-1080p.html">
                      WEBDL-1080p</a>
                                  </div>
                                  <div class="panel-footer">
                    <div class="row">
                      <div class="col-xs-6 col-sm-12 col-md-6 col-lg-6 text-left">
                        <a href="/catalogo/calidad.html" class="btn btn-link btn-sm btn-block"><i class="icon-list-alt"></i>  Ver todas las categorías</a>
                      </div>
                    </div>
                  </div>
                              </div>
                      <!--<div class="panel panel-primary">
  <div class="panel-heading">
    <h2 class="panel-title">Gracias por tu apoyo</h2>
  </div>
  <div class="panel-body text-center">
    <form target="_top" method="post" action="https://www.paypal.com/cgi-bin/webscr">
      <input type="hidden" value="_s-xclick" name="cmd">
      <input type="hidden" value="J4BTKN2NKH6P2" name="hosted_button_id">
      <input type="image" border="0" alt="PayPal - The safer, easier way to pay online!" name="submit" src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif">
      <img width="1" border="0" height="1" src="https://www.paypalobjects.com/es_XC/i/scr/pixel.gif" alt="">
    </form>
  </div>

</div>-->



        </div>
        <div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">
          <!-- breadcrumbs
          --------------------------------------------------------------->
          <ul class="breadcrumb">
            <li><a href="/" title="Ir a la  página de inicio">Inicio</a><span class="divider"></span></li>
            <li><a href="/catalogo/calidad.html">Calidad</a><span class="divider"></span></li><li class="active">3D</li>          </ul>
          <!-- breadcrumbs ^^^^^^^^^^^^^^^^^^^^^^^^^^^^-------------------->
                    <div class="col-xs-12 ">
            <img  class="img-responsive" src="/images/categorias/banner/9992.png" alt="" />
          </div>
                      <div id="calugas">
            <div class="row">
  <div class="col-xs-12 col-md-5">
    <h1>Calidad <small>3D</small></h1>
  </div>
  <div class="col-xs-12 col-lg-7 text-right">
    <div class="btn-toolbar">
      <div style="margin:16px 0" class="btn-group">
        <button type="button" class="btn btn-primary btn-lg" title="Orden por fecha" onclick="orden_orden();"><i class="icon-sort-by-order-alt"></i></button>
        <button type="button" class="btn btn-default btn-lg" title="Orden por Valoración" onclick="orden_rate();"><i class="icon-sort-by-attributes-alt"></i></button>
        <button type="button" class="btn btn-default btn-lg" title="Orden por Nombre" onclick="orden_nombre();"><i class="icon-sort-by-alphabet"></i></button>
      </div>
      <div id="paginador"></div>
    </div>
  </div>
</div>


<div class="container-folio row">
        <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/teenage-mutant-ninja-turtles-2014-3D.html' class="product-image" title="Teenage Mutant Ninja Turtles" data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/teenage-mutant-ninja-turtles-2014-3D.html' class="product-image" title="Teenage Mutant Ninja Turtles" data-toggle="">
    <img
      class="img-responsive"  alt="Teenage Mutant Ninja Turtles" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-201877.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201877" data-score="5.9"> </div>

    <h4><a class="titulo " href='/movie/teenage-mutant-ninja-turtles-2014-3D.html' title="Teenage Mutant Ninja Turtles" data-toggle="" >Teenage Mutant Ninja Turtles </a>
    </h4>
    <div class="desc">Misteriosos. Peligrosos. Reptilosos. Nunca has visto héroes como estos.</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/teenage-mutant-ninja-turtles-2014-3D.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/teenage-mutant-ninja-turtles-2014-3D.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2014&nbsp;<span class="icon-calendar"></span><br/>
          101'&nbsp;<span class="icon-time"></span><br/>
          4.3 GB&nbsp;<span class="icon-hdd"></span><br/>
          1.037&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/problem-child-1990.html' class="product-image" title="Problem Child" data-toggle="" >
    <img class="img-responsive"  alt="720p"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/720p-185.png' />
  </a>
  <a href='/movie/problem-child-1990.html' class="product-image" title="Problem Child" data-toggle="">
    <img
      class="img-responsive"  alt="Problem Child" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-201851.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201851" data-score="5.2"> </div>

    <h4><a class="titulo " href='/movie/problem-child-1990.html' title="Problem Child" data-toggle="" >Problem Child </a>
    </h4>
    <div class="desc">Attila the Hun. Ivan the Terrible. Al Capone. They were all seven once.</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/problem-child-1990.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/problem-child-1990.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>1990&nbsp;<span class="icon-calendar"></span><br/>
          81'&nbsp;<span class="icon-time"></span><br/>
          2.67 GB&nbsp;<span class="icon-hdd"></span><br/>
          2.219&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/avengers-age-of-ultron-2015-3d-hou.html' class="product-image" title="Avengers: Age of Ultron 3D HOU" data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/avengers-age-of-ultron-2015-3d-hou.html' class="product-image" title="Avengers: Age of Ultron 3D HOU" data-toggle="">
    <img
      class="img-responsive"  alt="Avengers: Age of Ultron 3D HOU" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-201857_1.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201857" data-score="7.9"> </div>

    <h4><a class="titulo " href='/movie/avengers-age-of-ultron-2015-3d-hou.html' title="Avengers: Age of Ultron 3D HOU" data-toggle="" >Avengers: Age of Ultron 3D HOU </a>
    </h4>
    <div class="desc">A New Age Has Come.</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/avengers-age-of-ultron-2015-3d-hou.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/avengers-age-of-ultron-2015-3d-hou.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2015&nbsp;<span class="icon-calendar"></span><br/>
          141'&nbsp;<span class="icon-time"></span><br/>
          23.46 GB&nbsp;<span class="icon-hdd"></span><br/>
          6.715&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/mad-max-fury-road-2015-3D.html' class="product-image" title="Mad Max: Fury Road" data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/mad-max-fury-road-2015-3D.html' class="product-image" title="Mad Max: Fury Road" data-toggle="">
    <img
      class="img-responsive"  alt="Mad Max: Fury Road" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-201782.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201782" data-score="8.4"> </div>

    <h4><a class="titulo " href='/movie/mad-max-fury-road-2015-3D.html' title="Mad Max: Fury Road" data-toggle="" >Mad Max: Fury Road </a>
    </h4>
    <div class="desc">El mundo se vuelve loco</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/mad-max-fury-road-2015-3D.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/mad-max-fury-road-2015-3D.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2015&nbsp;<span class="icon-calendar"></span><br/>
          120'&nbsp;<span class="icon-time"></span><br/>
          4.41 GB&nbsp;<span class="icon-hdd"></span><br/>
          9.218&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/home-2015-3D.html' class="product-image" title="Home" data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/home-2015-3D.html' class="product-image" title="Home" data-toggle="">
    <img
      class="img-responsive"  alt="Home" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-201693.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201693" data-score="6.8"> </div>

    <h4><a class="titulo " href='/movie/home-2015-3D.html' title="Home" data-toggle="" >Home </a>
    </h4>
    <div class="desc">Worlds Collide</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/home-2015-3D.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/home-2015-3D.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2015&nbsp;<span class="icon-calendar"></span><br/>
          94'&nbsp;<span class="icon-time"></span><br/>
          1.57 GB&nbsp;<span class="icon-hdd"></span><br/>
          9.216&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/the-spongebob-movie-sponge-out-of-water-2015-3D.html' class="product-image" title="The SpongeBob Movie: Sponge Out of Water" data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/the-spongebob-movie-sponge-out-of-water-2015-3D.html' class="product-image" title="The SpongeBob Movie: Sponge Out of Water" data-toggle="">
    <img
      class="img-responsive"  alt="The SpongeBob Movie: Sponge Out of Water" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-201591.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201591" data-score="6.5"> </div>

    <h4><a class="titulo " href='/movie/the-spongebob-movie-sponge-out-of-water-2015-3D.html' title="The SpongeBob Movie: Sponge Out of Water" data-toggle="" >The SpongeBob Movie: Sponge Out of Water </a>
    </h4>
    <div class="desc">He's leaving his world behind, to redeem himself of these past 10 years</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/the-spongebob-movie-sponge-out-of-water-2015-3D.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/the-spongebob-movie-sponge-out-of-water-2015-3D.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2015&nbsp;<span class="icon-calendar"></span><br/>
          92'&nbsp;<span class="icon-time"></span><br/>
          4.51 GB&nbsp;<span class="icon-hdd"></span><br/>
          8.384&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/jupiter-ascending-2015-3D.html' class="product-image" title="Jupiter Ascending" data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/jupiter-ascending-2015-3D.html' class="product-image" title="Jupiter Ascending" data-toggle="">
    <img
      class="img-responsive"  alt="Jupiter Ascending" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-201554.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201554" data-score="5.9"> </div>

    <h4><a class="titulo " href='/movie/jupiter-ascending-2015-3D.html' title="Jupiter Ascending" data-toggle="" >Jupiter Ascending </a>
    </h4>
    <div class="desc">Expand your universe.</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/jupiter-ascending-2015-3D.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/jupiter-ascending-2015-3D.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2015&nbsp;<span class="icon-calendar"></span><br/>
          127'&nbsp;<span class="icon-time"></span><br/>
          11.31 GB&nbsp;<span class="icon-hdd"></span><br/>
          9.634&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/monsters-inc-2001-3D.html' class="product-image" title="Monsters, Inc." data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/monsters-inc-2001-3D.html' class="product-image" title="Monsters, Inc." data-toggle="">
    <img
      class="img-responsive"  alt="Monsters, Inc." title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-201543.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201543" data-score="8.1"> </div>

    <h4><a class="titulo " href='/movie/monsters-inc-2001-3D.html' title="Monsters, Inc." data-toggle="" >Monsters, Inc. </a>
    </h4>
    <div class="desc">Asustamos porque nos importa.</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/monsters-inc-2001-3D.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/monsters-inc-2001-3D.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2001&nbsp;<span class="icon-calendar"></span><br/>
          92'&nbsp;<span class="icon-time"></span><br/>
          1.61 GB&nbsp;<span class="icon-hdd"></span><br/>
          5.426&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/seventh-son-2014-3D.html' class="product-image" title="Seventh Son" data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/seventh-son-2014-3D.html' class="product-image" title="Seventh Son" data-toggle="">
    <img
      class="img-responsive"  alt="Seventh Son" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-201512.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201512" data-score="5.6"> </div>

    <h4><a class="titulo " href='/movie/seventh-son-2014-3D.html' title="Seventh Son" data-toggle="" >Seventh Son </a>
    </h4>
    <div class="desc">When darkness falls, the son will rise. When the son falls, the dark knight will rise.</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/seventh-son-2014-3D.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/seventh-son-2014-3D.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2014&nbsp;<span class="icon-calendar"></span><br/>
          102'&nbsp;<span class="icon-time"></span><br/>
          10.04 GB&nbsp;<span class="icon-hdd"></span><br/>
          8.333&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/hotel-transylvania-2012-3D.html' class="product-image" title="Hotel Transylvania" data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/hotel-transylvania-2012-3D.html' class="product-image" title="Hotel Transylvania" data-toggle="">
    <img
      class="img-responsive"  alt="Hotel Transylvania" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-201509.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201509" data-score="7.1"> </div>

    <h4><a class="titulo " href='/movie/hotel-transylvania-2012-3D.html' title="Hotel Transylvania" data-toggle="" >Hotel Transylvania </a>
    </h4>
    <div class="desc">Donde los monstruos van para descansar en paz</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/hotel-transylvania-2012-3D.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/hotel-transylvania-2012-3D.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2012&nbsp;<span class="icon-calendar"></span><br/>
          91'&nbsp;<span class="icon-time"></span><br/>
          1.52 GB&nbsp;<span class="icon-hdd"></span><br/>
          9.271&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/penguins-of-madagascar-2014-3D.html' class="product-image" title="Penguins of Madagascar" data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/penguins-of-madagascar-2014-3D.html' class="product-image" title="Penguins of Madagascar" data-toggle="">
    <img
      class="img-responsive"  alt="Penguins of Madagascar" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-tt1911658.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201437" data-score="6.8"> </div>

    <h4><a class="titulo " href='/movie/penguins-of-madagascar-2014-3D.html' title="Penguins of Madagascar" data-toggle="" >Penguins of Madagascar </a>
    </h4>
    <div class="desc">Los mejores espías llevan esmoquin de serie.</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/penguins-of-madagascar-2014-3D.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/penguins-of-madagascar-2014-3D.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2014&nbsp;<span class="icon-calendar"></span><br/>
          92'&nbsp;<span class="icon-time"></span><br/>
          5.06 GB&nbsp;<span class="icon-hdd"></span><br/>
          8.090&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
            <div class="col-xs-6 col-xsm-4 col-sm-4 col-md-3 col-md-3">
        <div class="thumbnail">
  <a href='/movie/the-hobbit-the-battle-of-the-five-armies-2014-3D.html' class="product-image" title="The Hobbit: The Battle of the Five Armies" data-toggle="" >
    <img class="img-responsive"  alt="3D"  title="Audio Latino Torrent"
         src='http://img.alt-torrent.com/3D-185.png' />
  </a>
  <a href='/movie/the-hobbit-the-battle-of-the-five-armies-2014-3D.html' class="product-image" title="The Hobbit: The Battle of the Five Armies" data-toggle="">
    <img
      class="img-responsive"  alt="The Hobbit: The Battle of the Five Armies" title="Audio Latino Torrent"
      src='http://img.alt-torrent.com/productos/ficha/w185/w185-tt2310332.jpg'      />
  </a>
  <div class="caption">
    <div class="star hidden-xs" id="star_201429" data-score="7.6"> </div>

    <h4><a class="titulo " href='/movie/the-hobbit-the-battle-of-the-five-armies-2014-3D.html' title="The Hobbit: The Battle of the Five Armies" data-toggle="" >The Hobbit: The Battle of the Five Armies </a>
    </h4>
    <div class="desc">El capitulo decisivo.</div>
    <div class="row">
      <div class="col-xs-5 hidden-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/the-hobbit-the-battle-of-the-five-armies-2014-3D.html' class="btn btn-le btn-info"><span class="icon-film"></span> Info</a>
        </div>
      </div>
      <div class="col-xs-5 visible-lg">
        <div style="margin-bottom: 10px;">
          <a href='/movie/the-hobbit-the-battle-of-the-five-armies-2014-3D.html' class="btn btn-le btn-info" data-toggle=""><span class="icon-film" ></span> Ver Info</a>
        </div>
      </div>
      <div class="col-xs-7 hidden-xs text-right">
        <p>2014&nbsp;<span class="icon-calendar"></span><br/>
          144'&nbsp;<span class="icon-time"></span><br/>
          10.61 GB&nbsp;<span class="icon-hdd"></span><br/>
          8.551&nbsp;<span class="icon-eye-open"></span></p>

      </div>

    </div>
  </div>
</div>

      </div>
      </div>

<div class="row">
  <div class=".col-md-6 .col-md-offset-6 text-right">
      <div id="paginador2"></div>
  </div>
</div>
<script type="text/javascript" src="/lib/js/jquery.js"></script>
<script type="text/javascript" src="/lib/js/bootstrap-paginator.js"></script>
<script type='text/javascript'>
          var datos = {pagina: 1,
            mega_id:3,
            cat_id:'9992',
            subcat_id:'',
            titulo:'Calidad',
            orden:'orden',
            ancho:'185,278',
            alto:123.333333333,
            cat_nombre:'3D'};

          $(document).ready(function() {


            var options = {
              currentPage: 1,
              totalPages: 10,
              alignment: 'right',
              numberOfPages: 5,
              onPageClicked: function(e, originalEvent, type, page) {
                datos['pagina'] = page;
                $.ajax({
                  type: "POST",
                  url: "/bloque/thumbnails_categoria.php",
                  data: datos,
                  success: function(data) {
                    $('#calugas').html(data);
                  }
                });
              }
            };

            $('#paginador').bootstrapPaginator(options);
            $('#paginador2').bootstrapPaginator(options);
          });

          function orden_rate() {
            datos['orden'] = 'rate';
            $.ajax({
              type: "POST",
              url: "/bloque/thumbnails_categoria.php",
              data: datos,
              success: function(data) {

                $('#calugas').html(data);
              }
            });
          }

          function orden_nombre() {
            datos['orden'] = 'nombre';
            $.ajax({
              type: "POST",
              url: "/bloque/thumbnails_categoria.php",
              data: datos,
              success: function(data) {

                $('#calugas').html(data);
              }
            });
          }


          function orden_orden() {
            datos['orden'] = 'orden';
            $.ajax({
              type: "POST",
              url: "/bloque/thumbnails_categoria.php",
              data: datos,
              success: function(data) {

                $('#calugas').html(data);
              }
            });
          }

</script>
          </div>
        </div>
      </div>
      <hr />
    </div>
    <div class="panel-footer">
  <div class="container">
    <hr>
    <div class="row text-center">
      <address>&copy;2015. Derechos reservados. Alt-Torrent - Powered by <strong>ZeiZ</strong></address>
    </div>
  </div>
</div>
<a href="#" class="scrollup"></a>

<div class="modal fade" id="mensaje" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-body">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <span id="msgmodal">Texto</span>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-primary"data-dismiss="modal" >Aceptar</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->

<div id="message" class="hidden-sm hidden-xs">
  <a href="#" id="message_btn">Mensaje</a>
  <div class="caja_news">
    <h5>Problemas para descargar?</h5>
    <ul>
      <li>
        Si le das click a la descarga y no hace nada, es porque debes habilitar los popup para el sitio...<br>
      </li>
      <li>
        Si llegas a la página de adfly y quedas esperando los 5 seg aunque le des click a saltar publicidad es porque tienes instalado adblock y debes deshabilitarlo.
      </li>
    </ul>
    <!--<button id="newsletter_suscribirse">Suscribirse</button>-->
  </div>
</div>

<link rel="stylesheet" type="text/css" href="/lib/css/bootstrap.css" media="all" />
<link rel="stylesheet" type="text/css" href="/lib/css/bootstrap-theme.css" media="all" />
<link rel="stylesheet" type="text/css" href="/lib/css/font-awesome.css" media="all" />
<link rel="stylesheet" type="text/css" href="/lib/css/mCustomScrollbar.css" media="all" />
<link rel="stylesheet" type="text/css" href="/lib/css/fancybox.css" media="all" />
<link rel="stylesheet" type="text/css" href="/lib/css/helpers/jquery.fancybox-buttons.css"  media="all" />
<link rel="stylesheet" type="text/css" href="/lib/css/helpers/jquery.fancybox-thumbs.css?v=1.0.7" media="screen" />
<link rel="stylesheet" type="text/css" href="/themes/audiolatino/css/theme.css" media="all" />



<script type="text/javascript" src="/lib/js/raty.js"></script>
<script type="text/javascript">
        $('#star_201877').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 5.9        });
              $('#star_201851').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 5.2        });
              $('#star_201857').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 7.9        });
              $('#star_201782').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 8.4        });
              $('#star_201693').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 6.8        });
              $('#star_201591').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 6.5        });
              $('#star_201554').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 5.9        });
              $('#star_201543').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 8.1        });
              $('#star_201512').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 5.6        });
              $('#star_201509').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 7.1        });
              $('#star_201437').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 6.8        });
              $('#star_201429').raty({
          readOnly: true
          , space: false
          , number: 10
          , starHalf: '/lib/images/star-half-small.png'
          , starOff: '/lib/images/star-off-small.png'
          , starOn: '/lib/images/star-on-small.png'
          , score: 7.6        });

  function orden_rate() {
    datos['orden'] = 'rate';
    $.ajax({
      type: "POST",
      url: "/bloque/thumbnails_categoria.php",
      data: datos,
      success: function (data) {

        $('#calugas').html(data);
      }
    });
  }

  function orden_nombre() {
    datos['orden'] = 'nombre';
    $.ajax({
      type: "POST",
      url: "/bloque/thumbnails_categoria.php",
      data: datos,
      success: function (data) {

        $('#calugas').html(data);
      }
    });
  }


  function orden_orden() {
    datos['orden'] = 'orden';
    $.ajax({
      type: "POST",
      url: "/bloque/thumbnails_categoria.php",
      data: datos,
      success: function (data) {

        $('#calugas').html(data);
      }
    });
  }
</script>
<script type="text/javascript" src="/lib/js/holder.js"></script>
<script type="text/javascript" src="/lib/js/validate.js"></script>
<script type="text/javascript" src="/lib/js/mousewheel.js"></script>
<script type="text/javascript" src="/lib/js/mCustomScrollbar.js"></script>
<script type="text/javascript" src="/lib/js/bootstrap.js"></script>
<script type="text/javascript" src="/lib/js/bootpag.js"></script>
<script type="text/javascript" src="/lib/js/bootstrap-paginator.js"></script>
<script type="text/javascript" src="/lib/js/bootstrap-validation.js"></script>
<script type="text/javascript" src="/lib/js/fancybox.js"></script>
<script type="text/javascript" src="/lib/js/helpers/jquery.fancybox-buttons.js?v=1.0.5"></script>
<script type="text/javascript" src="/lib/js/helpers/jquery.fancybox-thumbs.js?v=1.0.7"></script>
<script type="text/javascript" src="/lib/js/helpers/jquery.fancybox-media.js?v=1.0.6"></script>
<script type="text/javascript" src="/lib/js/cookies.js"></script>
<script type="text/javascript" src="/lib/js/cloud-zoom.1.0.3.js"></script>
<script type="text/javascript" src="/lib/js/jquery.jscrollpane.min.js"></script>
<style>
  .navbar-default {
    background-color: #f4f4f4;;
    border-color: #eed3d7;}
  .navbar-default .navbar-brand {
    color: #ffffff;
  }
  .navbar-default .navbar-nav > li > a {
    color: #ffffff;
  }
  .navbar-default .navbar-nav > .dropdown > a .caret {
    border-bottom-color: #ffffff;
    border-top-color: #ffffff;
  }

  .navbar-default {
    background-image: -webkit-gradient(linear, left 0%, left 100%, from(#ee4036), to(#de1e13));
    background-image: -webkit-linear-gradient(top, #ee4036, 0%, #de1e13, 100%);
    background-image: -moz-linear-gradient(top, #ee4036 0%, #de1e13 100%);
    background-image: linear-gradient(to bottom, #ee4036 0%, #de1e13 100%);
    background-repeat: repeat-x;
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffee4036', endColorstr='#ffde1e13', GradientType=0);
    border-radius: 4px;
  }

  .dropdown-menu > li > a:hover,
  .dropdown-menu > li > a:focus,
  .dropdown-menu > .active > a,
  .dropdown-menu > .active > a:hover,
  .dropdown-menu > .active > a:focus {
    background-image: -webkit-gradient(linear, left 0%, left 100%, from(#ee4036), to(#de1e13));
    background-image: -webkit-linear-gradient(top, #ee4036, 0%, #de1e13, 100%);
    background-image: -moz-linear-gradient(top, #ee4036 0%, #de1e13 100%);
    background-image: linear-gradient(to bottom, #ee4036 0%, #de1e13 100%);
    background-repeat: repeat-x;
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffee4036', endColorstr='#ffde1e13', GradientType=0);
    background-color: #415b8e;
  }

  .pagination .nolatino> .active > a,
  .pagination .nolatino> .active > span,
  .pagination .nolatino> .active > a:hover,
  .pagination .nolatino> .active > span:hover,
  .pagination .nolatino> .active > a:focus,
  .pagination .nolatino> .active > span:focus {
    background-color: #ee4036 ;
    border-color: #ee4036 ;
    color: #ffffff;
    cursor: default;
    z-index: 2;
  }

.pagination .nolatino> li > a, .pagination .nolatino> li > span {
    background-color: #ffffff;
    border: 1px solid #dddddd;
     color:#ee4036;
}

  .nolatino {
    color:#ee4036;
  }
</style>
<!--    <script type="text/javascript">

      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', '']);
      _gaq.push(['_trackPageview']);

      (function() {
        var ga = document.createElement('script');
        ga.type = 'text/javascript';
        ga.async = true;
        ga.src = ('https:' === document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(ga, s);
      })();

    </script>-->
    <script>
      (function(i, s, o, g, r, a, m) {
        i['GoogleAnalyticsObject'] = r;
        i[r] = i[r] || function() {
          (i[r].q = i[r].q || []).push(arguments)
        }, i[r].l = 1 * new Date();
        a = s.createElement(o),
                m = s.getElementsByTagName(o)[0];
        a.async = 1;
        a.src = g;
        m.parentNode.insertBefore(a, m);
      })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

      ga('create', 'UA-46441407-2', 'www.alt-torrent.com');
      ga('require', 'linkid', 'linkid.js');
      ga('send', 'pageview');
      ga('set', '&uid', '136330'); // Establezca el ID de usuario mediante el user_id con el que haya iniciado sesión.

    </script>

<script type="text/javascript">
//<![CDATA[
  Mage.Cookies.path = '/themes/default';
  Mage.Cookies.domain = 'www.alt-torrent.com';

  $(document).ready(function () {

    $(window).scroll(function () {
      if ($(this).scrollTop() > 100) {
        $('.scrollup').fadeIn();
      } else {
        $('.scrollup').fadeOut();
      }
    });

    $('.scrollup').click(function () {
      $("html, body").animate({scrollTop: 0}, 600);
      return false;
    });



    $('#login_form').validate({
      rules: {
        user: {
          required: true,
          remote: {
            url: "/ajax/login_check_user.php",
            type: "post"
          }
        },
        password: {
          minlength: 6,
          required: true,
          remote: {
            url: "/ajax/login_check_pass.php",
            type: "post",
            data: {
              user: function () {
                return $("#user").val();
              }
            }
          }
        }
      },
      messages: {
        user: {
          remote: "Usuario no existe"
        },
        password: {
          remote: "Contraseña incorrecta"
        }
      },
      highlight: function (element) {
        $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
      },
      success: function (element) {
        element.closest('.form-group').removeClass('has-error').addClass('has-success');
      },
      errorElement: 'span',
      errorClass: 'help-block',
      errorPlacement: function (error, element) {
        if (element.parent('.input-group').length) {
          error.insertAfter(element.parent());
        } else {
          error.insertAfter(element);
        }
      },
      submitHandler: function (form) {
        var data = jQuery('#login_form').serialize();
        url = jQuery('#login_form').attr('action');
        jQuery.ajax({url: '/ajax/login_check.php',
          dataType: 'json',
          type: 'post',
          data: data,
          success: function (r) {
            if (r) {
              window.location.href = "/";
            } else {
              jQuery('.messages').replaceWith(data.mensaje);
            }

          }
        });
      }
    });

    $('#signup_form').validate({
      rules: {
        s_username: {
          required: true,
          minlength: 4,
          maxlength: 20,
          remote: {
            url: "/ajax/signup_user_check.php",
            type: "post"
          }
        },
        s_email: {
          required: true,
          email: true,
          remote: {
            url: "/ajax/signup_email_check.php",
            type: "post"
          }
        },
        s_password: {
          minlength: 6,
          required: true
        },
        s_password2: {equalTo: "#s_password"},
        dia: {required: true, range: [1, 31]},
        mes: {required: true, range: [1, 13]},
        ano: {required: true, min: 1950},
        gender: {required: true},
        terminos: {required: true}
      },
      messages: {
        s_username: {
          remote: "Usuario ya existe"
        },
        s_email: {
          remote: "E-Mail ya esta registrado"
        }
      },
      highlight: function (element) {
        $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
      },
      success: function (element) {
        element.closest('.form-group').removeClass('has-error').addClass('has-success');
      },
      errorElement: 'span',
      errorClass: 'help-block',
      errorPlacement: function (error, element) {
        if (element.parent('.input-group').length) {
          error.insertAfter(element.parent());
        } else {
          error.insertAfter(element);
        }
      },
      submitHandler: function (form) {
        var data = jQuery('#signup_form').serialize();
        url = jQuery('#signup_form').attr('action');
        $.post(url, data,
                function (data) {
                  datos = JSON.parse(data);
                  if (datos.id) {
                    $('#namelogin').html(datos.username);
                    $('#Signup').modal('hide');
                    $('#Signup-succes').modal('show');
                  }
                }
        );
      }
    });

    $('#message_btn').on('click', function (e) {
      e.preventDefault();
      if ($("#message").css('right') === '-663px') {
        $("#message").stop().animate({right: '0px'}, 'fast');
      }
      ;
      if ($("#message").css('right') === '0px') {
        $("#message").stop().animate({right: '-663px'}, 'normal');
      }
      ;
    });

  });


  function signup() {

    $('#Login').modal('hide');
    $('#Signup').modal({
      show: true
    });
  }

  function forgot() {
    $('#Login').modal('hide');
    $('#Forgot').modal({
      show: true
    });
  }

  $('#forgotForm').validate({
    rules: {
      codigo: {
        required: true,
        remote: {
          url: "/ajax/forgot_check_codigo.php",
          type: "post"
        }
      },
      f_newpass1: {
        minlength: 6,
        required: true
      },
      f_newpass2: {equalTo: "#f_newpass1"}
    },
    messages: {codigo: {remote: "Código no corrresponde"}},
    highlight: function (element) {
      $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
    },
    success: function (element) {
      element.closest('.form-group').removeClass('has-error').addClass('has-success');
    },
    debug:true,
    errorElement: 'span',
    errorClass: 'help-block',
    errorPlacement: function (error, element) {
      if (element.parent('.input-group').length) {
        error.insertAfter(element.parent());
      } else {
        error.insertAfter(element);
      }
    }
  });

  function forgotSubmit() {
    if ($("#forgotForm").validate()) {
      var data = jQuery('#forgotForm').serialize();
      jQuery.ajax({url: '/ajax/forgot_change_pass.php',
        dataType: 'json',
        type: 'post',
        data: data,
        success: function (r) {
          $('#Forgot').modal('hide');
          $('#Login').modal({
            show: true
          });
        }
      });
    }
  }

  function sendcode() {
    $('#Forgot').modal('hide');
    $('#SendCode').modal({
      show: true
    });
  }

  $('#sendcodeForm').validate({
    rules: {
      email: {
        required: true,
        remote: {
          url: "/ajax/login_check_email.php",
          type: "post"
        }
      }
    },
    messages: {email: {remote: "E-Mail no esta registrado"}},
    highlight: function (element) {
      $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
    },
    success: function (element) {
      element.closest('.form-group').removeClass('has-error').addClass('has-success');
    },
    errorElement: 'span',
    errorClass: 'help-block',
    errorPlacement: function (error, element) {
      if (element.parent('.input-group').length) {
        error.insertAfter(element.parent());
      } else {
        error.insertAfter(element);
      }
    }
  });

  function sendcodeSubmit() {
    if ($("#sendcodeForm").validate()) {
      var data = $('#sendcodeForm').serialize();
      $.ajax({url: '/ajax/forgot_pass.php',
        dataType: 'json',
        type: 'post',
        data: data,
        success: function (r) {
          $('#SendCode').modal('hide');
          $('#Forgot').modal({
            show: true
          });
        }
      });
    }
  }





  function logout() {
    $.get("/ajax/logout.php", function (data) {
    });

  }

  function setAjaxData(data, iframe, fancybox) {
    if (data.status === 'ERROR') {
      alert(data.message);
    }
    if (data.status === 'SUCCESS') {
      if (data.message) {
        messagemodal('<span id="msgmodal">' + data.message + '<span>');
      }
      if (jQuery('#tooltipcarro')) {
        jQuery('#tooltipcarro').replaceWith(data.tooltipcarro);
      }
      if (jQuery('#totalcarro')) {
        jQuery('#totalcarro').replaceWith(data.totalcarro);
      }
    }
  }

  function messagemodal(message) {
    jQuery('#msgmodal').replaceWith(message);
    $('#mensaje').modal('show');
  }


  function showOptions(id) {
    jQuery('#fancybox' + id).trigger('click');
  }

  function onepageLogin(button, submit) {
    if (loginForm.validator && loginForm.validator.validate()) {
      button.disabled = true;
      if (submit)
        loginForm.submit();
      var data = jQuery('#login-form').serialize();
      url = jQuery('#login-form').attr('action');
      jQuery.ajax({url: url,
        dataType: 'json',
        type: 'post',
        data: data,
        success: function (data) {
          jQuery('#ajax_loader').hide();
          parent.setAjaxData(data, true, true);
          if (data.messages) {
            jQuery('.messages').replaceWith(data.messages);
          }

          if (data.ok) {
            if (data.location) {
              document.login_form.action = data.location;
              jQuery('#login-form').submit();
            }
          }
        }
      });
      button.disabled = false;
    }
  }

  function screensize() {
    jQuery('#screensize').replaceWith('<div id="screensize" class="navbar-fixed-top">' + $(document).width() + 'x' + $(document).height() + '<\/DIV>');
  }
  // window.onresize = screensize;

  $.fn.scrollLoad = function (options) {

    var defaults = {
      url: '',
      data: '',
      ScrollAfterHeight: 90,
      onload: function (data, itsMe) {
        alert(data);
      },
      start: function (itsMe) {
      },
      continueWhile: function () {
        return true;
      },
      getData: function (itsMe) {
        return '';
      }
    };

    for (var eachProperty in defaults) {
      if (options[ eachProperty ]) {
        defaults[ eachProperty ] = options[ eachProperty ];
      }
    }

    return this.each(function () {
      this.scrolling = false;
      this.scrollPrev = this.onscroll ? this.onscroll : null;
      $(this).bind('scroll', function (e) {
        if (this.scrollPrev) {
          this.scrollPrev();
        }
        if (this.scrolling)
          return;
        //var totalPixels = $( this ).attr( 'scrollHeight' ) - $( this ).attr( 'clientHeight' );
        if (Math.round($(this).attr('scrollTop') / ($(this).attr('scrollHeight') - $(this).attr('clientHeight')) * 100) > defaults.ScrollAfterHeight) {
          defaults.start.call(this, this);
          this.scrolling = true;
          $this = $(this);
          $.ajax({url: defaults.url, data: defaults.getData.call(this, this), type: 'post', success: function (data) {
              $this[ 0 ].scrolling = false;
              defaults.onload.call($this[ 0 ], data, $this[ 0 ]);
              if (!defaults.continueWhile.call($this[ 0 ], data)) {
                $this.unbind('scroll');
              }
            }});
        }
      });
    });
  };

  $("input,select,textarea").jqBootstrapValidation();


  $('.button-checkbox').each(function () {

    // Settings
    var $widget = $(this),
            $button = $widget.find('button'),
            $checkbox = $widget.find('input:checkbox'),
            color = $button.data('color'),
            settings = {
              on: {
                icon: 'glyphicon glyphicon-check'
              },
              off: {
                icon: 'glyphicon glyphicon-unchecked'
              }
            };

    // Event Handlers
    $button.on('click', function () {
      $checkbox.prop('checked', !$checkbox.is(':checked'));
      document.getElementById("submit_signup").disabled = !$checkbox.is(':checked');
      $checkbox.triggerHandler('change');
      updateDisplay();
    });
    $checkbox.on('change', function () {
      updateDisplay();
    });

    // Actions
    function updateDisplay() {
      var isChecked = $checkbox.is(':checked');

      // Set the button's state
      $button.data('state', (isChecked) ? "on" : "off");

      // Set the button's icon
      $button.find('.state-icon')
              .removeClass()
              .addClass('state-icon ' + settings[$button.data('state')].icon);

      // Update the button's color
      if (isChecked) {
        $button
                .removeClass('btn-default')
                .addClass('btn-' + color + ' active');

      }
      else {
        $button
                .removeClass('btn-' + color + ' active')
                .addClass('btn-default');
      }
      $("#terminos").prop("checked", isChecked);
    }

    // Initialization
    function init() {

      updateDisplay();

      // Inject the icon if applicable
      if ($button.find('.state-icon').length === 0) {
        $button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i> ');
      }
    }
    init();
  });
</script>

<script type="text/javascript">
  var adfly_id = 7427278;
</script>


  </body>
</html>'''


import requests

url = "http://www.elitetorrent.net/categoria/1/estrenos/modo:listado/pag:1"
browser = requests.Session()
page = "1"
import bs4

response = browser.get( url + page)

soup = bs4.BeautifulSoup(response.text)
links = soup.select("a.nombre")
for link in links:
    print link.get("title", ""), link["href"]

# import re
#
# datos = re.search("var datos =(.*?);", data, re.DOTALL).group(1).replace("{", "").replace("}", "")
# params = {}
# for item in datos.split("\n"):
#     if item.strip() != "":
#         key, value = item.strip()[:-1].split(':')
#         params[key] = value.replace("'", "")
# #settings.debug(params)
# opciones = re.search("var options =(.*?);", data, re.DOTALL).group(1).replace("{", "").replace("}", "") + ": ''"
# params1 = {}
# for item in opciones.split("\n"):
#     if item.strip() != "":
#         key, value = item.strip()[:-1].split(':')
#         params1[key] = value.replace("'", "")
# #settings.debug(params1)
# urlPage = re.search('url: "(.*?)"', data).group(1)
