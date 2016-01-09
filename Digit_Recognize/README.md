# Digit_Recognize
* Introduction
<br>&nbsp;&nbsp;&nbsp;&nbsp;
Using sklearn.svm recognize digit image which are downloaded from MNIST database.
<br><br>
* OS
  * ubuntu 14.04 64-bit with kernel 3.19.0
<br><br>
* Requirement
  * Python 3.4.3
  * Numpy 1.10.2
  * sklearn 0.17
  * pylab 0.1.3
  <br><br>
* Installation
  * Python 3.4.3
  <br>&nbsp;&nbsp;&nbsp;&nbsp;
  `$ sudo apt-get install python3`
  * Numpy 1.10.2
  <br>&nbsp;&nbsp;&nbsp;&nbsp;
  `$ sudo pip3 install numpy`
  * sklearn 0.17
  <br>&nbsp;&nbsp;&nbsp;&nbsp;
  `$ sudo pip3 install sklearn`
  * pylab 0.1.3
  <br>&nbsp;&nbsp;&nbsp;&nbsp;
  `$ sudo pip3 install pylab`
<br><br>
* Usage
 <br>&nbsp;&nbsp;&nbsp;&nbsp;
 `$ python3 MnistClassifiers.py`
<br><br>
* Optimize
  * kernel : rbf, linear, poly, sigmoid. default=rbf
	  <table>
	    <tr>
	      <td></td>
	      <td><center> kernel='rbf' </center></td>
	      <td><center> kernel='linear' </center></td>
	      <td><center> kernel='poly' </center></td>
	      <td><center> kernel='sigmoid' </center></td>
	    </tr>
	    <tr>
	      <td><center> Avg Precision </center></td>
	      <td><center> 0.01 </center></td>
	      <td><center> 0.91 </center></td>
	      <td><center> <strong>0.94</strong> </center></td>
	      <td><center> 0.01 </center></td>
	    </tr>
	  </table>
  * C : float. default=1.0
  	<table>
  	  <tr>
  	    <td></td>
  	    <td><center> kernel='poly' C=1.0 </center></td>
  	    <td><center> kernel='poly' C=0.1 </center></td>
  	    <td><center> kernel='poly' C=4.0 </center></td>
  	  </tr>
  	  <tr>
  	    <td><center> Avg Precision </center></td>
  	    <td><center> <strong>0.94</strong> </center></td>
  	    <td><center> 0.94 </center></td>
  	    <td><center> 0.94 </center></td>
  	  </tr>
  	</table>
  * degree : int. default=3
  	<table>
  	  <tr>
  	    <td></td>
  	    <td><center> kernel='poly' degree=3 </center></td>
  	    <td><center> kernel='poly' degree=1 </center></td>
  	    <td><center> kernel='poly' degree=2 </center></td>
  	    <td><center> kernel='poly' degree=4 </center></td>
  	  </tr>
  	  <tr>
  	    <td><center> Avg Precision </center></td>
  	    <td><center> 0.94 </center></td>
  	    <td><center> 0.91 </center></td>
  	    <td><center> <strong>0.95</strong> </center></td>
  	    <td><center> 0.93 </center></td>
  	  </tr>
  	</table>
  * gamma: float. default=auto
  * coef0: float. default=0.0
  * probability : boolean. default=False
  * strinking : boolean. default=True
  * class_weight : { dict: 'balance' }
  * max_iter : int . default=-1(unlimit)
  * decision_function_shape : 'ovo', 'ovr' or None. default=None
  * random_state : int seed. default=None
  * tol : float. default=1e-3
<br><br>
* Contact
  <pre>
  Prof:   Renyuan Lyu
  E-mail: <a href='mailto:renyuan.lyu@gmail.com'>renyuan.lyu@gmail.com</a>
  
  Author: Jin Ye
  E-mail: <a href='mailto:don0910129285@gmail.com'>don0910129285@gmail.com</a>
  </pre>
