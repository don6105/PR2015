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
	      <td>kernel='rbf'</td>
	      <td>kernel='linear'</td>
	      <td>kernel='poly'</td>
	      <td>kernel='sigmoid'</td>
	    </tr>
	    <tr>
	      <td>Avg Precision</td>
	      <td>0.01</td>
	      <td>0.91</td>
	      <td><strong>0.94</strong></td>
				<td>0.01</td>
	    </tr>
	  </table>
  * C : float. default=1.0
  <table>
    <tr>
      <td></td>
			<td>kernel='poly' C=1.0</td>
      <td>kernel='poly' C=0.1</td>
			<td>kernel='poly' C=4.0</td>
    </tr>
    <tr>
      <td>Avg Precision</td>
			<td><strong>0.94</strong></td>
      <td>0.94</td>
      <td>0.94</td>
    </tr>
  </table>
  * degree : int. default=3
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
