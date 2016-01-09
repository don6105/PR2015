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
* Parameters Optimize
  * kernel : rbf, linear, poly, sigmoid. default=rbf
	  <table>
	    <tr>
	      <td></td>
	      <td> kernel='rbf' </td>
	      <td> kernel='linear' </td>
	      <td> kernel='poly' </center></td>
	      <td> kernel='sigmoid' </td>
	    </tr>
	    <tr>
	      <td> Avg Precision </td>
	      <td> 0.01 </td>
	      <td> 0.91 </td>
	      <td> <strong>0.94</strong> </td>
	      <td> 0.01 </td>
	    </tr>
	  </table>
  * C : float. default=1.0
  	<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' C=1.0 </td>
  	    <td> kernel='poly' C=0.1 </td>
  	    <td> kernel='poly' C=4.0 </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> <strong>0.94</strong> </td>
  	    <td> 0.94 </td>
  	    <td> 0.94 </td>
  	  </tr>
  	</table>
  * degree : int. default=3
  	<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' degree=3 </td>
  	    <td> kernel='poly' degree=1 </td>
  	    <td> kernel='poly' degree=2 </td>
  	    <td> kernel='poly' degree=4 </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> 0.94 </td>
  	    <td> 0.91 </td>
  	    <td> <strong>0.95</strong> </td>
  	    <td> 0.93 </td>
  	  </tr>
  	</table>
  * gamma: float. default=auto
   	<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' gamma=auto </td>
  	    <td> kernel='poly' gamma=0.1 </td>
  	    <td> kernel='poly' gamma=4.0 </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> <strong>0.94</strong> </td>
  	    <td> 0.94 </td>
  	    <td> 0.94 </td>
  	  </tr>
  	</table>
  * coef0: float. default=0.0
  	<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' coef0=0.0 </td>
  	    <td> kernel='poly' coef0=0.1 </td>
  	    <td> kernel='poly' coef0=4.0 </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> <strong>0.94</strong> </td>
  	    <td> 0.94 </td>
  	    <td> 0.94 </td>
  	  </tr>
  	</table>
  * probability : boolean. default=False
  	<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' probability=False </td>
  	    <td> kernel='poly' probability=True </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> <strong>0.94</strong> </td>
  	    <td> 0.94 </td>
  	  </tr>
  	</table>
  * strinking : boolean. default=True
  	<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' strinking=True </td>
  	    <td> kernel='poly' strinking=False </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> <strong>0.94</strong> </td>
  	    <td> 0.94 </td>
  	  </tr>
  	</table>
  * class_weight : { dict: 'balance' }
 		<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' class_weight=balance </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> <strong>0.94</strong> </td>
  	  </tr>
  	</table>
  * max_iter : int . default=-1(unlimit)
 		<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' max_iter=-1 </td>
  	    <td> kernel='poly' max_iter=1 </td>
  	    <td> kernel='poly' max_iter=4 </td>
  	    <td> kernel='poly' max_iter=100 </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> <strong>0.94</strong> </td>
  	    <td> 0.53 </td>
  	    <td> 0.54 </td>
  	    <td> 0.93 </td>
  	  </tr>
  	</table>
  * decision_function_shape : 'ovo', 'ovr' or None. default=None
 		<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' decision_function_shape=None </td>
  	    <td> kernel='poly' decision_function_shape='ovo' </td>
  	    <td> kernel='poly' decision_function_shape='ovr' </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> <strong>0.94</strong> </td>
  	    <td> 0.94 </td>
  	    <td> 0.94 </td>
  	  </tr>
  	</table>
  * random_state : int seed. default=None
 		<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' random_state=None </td>
  	    <td> kernel='poly' random_state=1 </td>
  	    <td> kernel='poly' random_state=4 </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> <strong>0.94</strong> </td>
  	    <td> 0.94 </td>
  	    <td> 0.94 </td>
  	  </tr>
  	</table>
  * tol : float. default=1e-3
 		<table>
  	  <tr>
  	    <td></td>
  	    <td> kernel='poly' tol=1e-3 </td>
  	    <td> kernel='poly' tol=3.0 </td>
  	    <td> kernel='poly' tol=2.0 </td>
  	    <td> kernel='poly' tol=1e-8 </td>
  	    <td> kernel='poly' tol=1e-12 </td>
  	  </tr>
  	  <tr>
  	    <td> Avg Precision </td>
  	    <td> <strong>0.94</strong> </td>
  	    <td> 0.01 </td>
  	    <td> 0.93 </td>
  	    <td> 0.94 </td>
  	    <td> 0.94 </td>
  	  </tr>
  	</table>
<br><br>
* Contact
  <pre>
  Prof:   Renyuan Lyu
  E-mail: <a href='mailto:renyuan.lyu@gmail.com'>renyuan.lyu@gmail.com</a>
  
  Author: Jin Ye
  E-mail: <a href='mailto:don0910129285@gmail.com'>don0910129285@gmail.com</a>
  </pre>
