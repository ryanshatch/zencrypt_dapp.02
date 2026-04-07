<!--
********************************************************************************************
* Title: Zencrypt WebApp           |********************************************************
* Developed by: Ryan Hatch         |********************************************************
  Date: August 10th 2022           |********************************************************
  Last Updated: February 13th 2025 |********************************************************
  Version: 5.3.3                   |********************************************************
********************************************************************************************
*-****************************** Zencrypt v5.3-A3 |*****************************************
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
|              Zencrypt Web-App is a Flask application that can be used to:                |
|       - Generate hashes: using SHA256 hashing algorithm, with an optional salt value.    |
|       - Encrypt text and files: using Fernet symmetric encryption algorithm.             |
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
-->

<div class="table-of-contents">
  <h1>Table of contents</h1>
  <h2>Webapp v5.3-A3</h2>
  <ul>
    <li><a href="README.md">What is Zencrypt</a></li>
    <li><a href="cipher/zencrypt-cli.md">Getting To Know About The Zencrypt CLI</a></li>
  </ul>
  <h2>Zencrypt Whitepapers</h2>
  <ul>
    <li>
      <a href="cipher-whitepapers/zencrypt-documentation/README.md">Zencrypt Documentation</a>
      <ul>
        <li>
          <a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/README.md">A Shorter Description About My Enhancement Plans for Zencrypt:</a>
          <ul>
            <li>
              <a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/software-engineering-and-design/README.md">Enhancing and Updating The Software Engineering and Design</a>
              <ul>
                <li><a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/software-engineering-and-design/explanation-of-key-flowchart.md">Key Flowchart Explanation</a></li>
              </ul>
            </li>
            <li>
              <a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/updating-zencrypt-algorithms-and-data-structures/README.md">Updating The Algorithms and Data Structures:</a>
              <ul>
                <li><a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/updating-zencrypt-algorithms-and-data-structures/flowchart-explanation.md">Flowchart Explanation</a></li>
              </ul>
            </li>
            <li>
              <a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/updating-zencrypt-databases/README.md">Enhancing the Database Management For Zencrypt</a>
              <ul>
                <li><a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/updating-zencrypt-databases/flowchart-explanation.md">Flowchart Explanation</a></li>
              </ul>
            </li>
            <li>
              <a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/skills-and-illustrated-outcomes/README.md">Skills and Illustrated Outcomes</a>
              <ul>
                <li><a href="cipher-whitepapers/zencrypt-documentation/a-shorter-description-about-my-enhancement-plan-for-zencrypt-cli/skills-and-illustrated-outcomes/eportfolio-in-current-state.md">ePortfolio</a></li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>
<hr>
<!--
*  ***************************#* Zencrypt v5.3-A3 |*****************************************
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
*******************************#* Description: |********************************************
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
|              Zencrypt Web-App is a Flask application that can be used to:                |
|       - Generate hashes: using SHA256 hashing algorithm, with an optional salt value.    |
|       - Encrypt text and files: using Fernet symmetric encryption algorithm.             |
<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
-->
<!DOCTYPE html>
<html>
  <body>
    <hr>
    <h1 align="center">Zencrypt</h1>
    <hr>
    <br>
    <p align="center">
      <strong>Webapp Release - v5.3-A3</strong>
<!--       <br>
      <strong>By: Ryan Hatch</strong> -->
      <br>
    </p>
    <p align="center">
      <a href="#introduction">Introduction</a> • <a href="#features">Features</a> • <a href="#installation">Installation</a> • <a href="#usage">Usage</a> • <a href="#examples">Examples</a> • <a href="#contributing">Contributing</a> • <a href="#disclaimer">Disclaimer</a> • <a href="#license">License</a> • <a href="#contact">Contact</a>
    </p>
    <hr>
    <p align="center">
<!--       <br> -->
      <strong>Developed By: Ryan Hatch</strong>
    <p align="center"> &copy; 2025 Ryan Hatch <br> All Rights Reserved.<br><i><br>This software is proprietary and owned by Ryan Hatch. Unauthorized use, modification, or distribution is prohibited.</i> </p>
    <h3>Logs of Recent Updates:</h3>
    <li>Jan 20 2025 - Updated comments and added a more simple structure for the changes to be made.</li>
    <li>Jan 21st 2025 - Merged the CLI into a webapp using the Flask framework. The current version is being hosted at <a href="https://zencrypt.app">Zencrypt.app</a></li>
    <li>Jan 22nd 2025 - Users can upload files for encryption and decryption.</li>
    <li>Jan 26th 2025 - Allows users to manage sessions by creating an account and logging in.</li>
    <li>Jan 27th 2025 - Fully merged MongoDB into the backend for user authentication and session management.</li>
    <li>Jan 28th 2025 - Created new schemas for the database to store user information and session data.</li>
    <hr>
    <h2 id="introduction">Introduction</h2>
    <p> Zencrypt is a webapp that allows users to hash, encrypt, and decrypt text and files. The webapp runs on the Flask framework and is hosted at <a href="https://zencrypt.app">Here.</a>
        <br>
        <p>The web app is built for simplicity and ease of use, allowing users to hash, encrypt, and decrypt text and files effortlessly. Future updates will include PGP encryption, fully integrating the CLI script’s capabilities into the web app. The backend uses MongoDB for user authentication, session management, and securely storing encrypted metadata while keeping user inputs in plain text.</p>
    <h2 id="features">Features</h2>
    <ul>
      <li>
        <strong>Generate SHA256 hashes</strong><i> with optional salt.</i>
      </li>
      <li>
        <strong>Encrypt and decrypt text.</strong>
      <li>
        <strong>Encrypt and decrypt files.</strong>
      </li>
    </ul>
    <h2 id="installation">Installation</h2>
    <p> To install Zencrypt, you will need to follow these steps: </p>
    <ol>
      <li>Clone the repository or download the source code with the command:<br><code>git clone https://github.com/imaclone.x/Zencrypt.git</code>. </li>
        <li>Navigate to the project directory with the command: <code>cd Zencrypt</code>. </li>
        <li>First, you will need to install Python 3.7 or higher. You can download Python from the official website: <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>. </li>
            <li>Next, you will need to install pip, the Python package manager. You can install pip by following the instructions on the official website: <a href="https://pip.pypa.io/en/stable/installation/">https://pip.pypa.io/en/stable/installation/</a>. </li>
            <li>Once you have installed Python and pip, you can create a virtual environment with the command: <code>python -m venv venv</code>. </li>
            <li>Activate the virtual environment with the command: <code>source venv/bin/activate</code> on Linux or <code>venv\Scripts\activate</code> on Windows. </li>
      <li>Install the required dependencies with the command: <code>pip install -r requirements.txt</code>. </li>
    </ol>
    <h2 id="usage">How to Run Locally:</h2>
    <p> To use the webapp, you will need to follow these steps: </p>
    <ol>
      <li>Run the webapp with the command: <code>python webapp.py</code>. </li>
      <li>Open a web browser and navigate to <code>http://localhost:5000</code>. </li>
      <li>Use the webapp to hash, encrypt, and decrypt text and files. </li>
    </ol>
    <h2 id="examples">Examples of CLI (v4-B1) Functionality:</h2>
    <h3 align="center">Hashing:</h3>
    <center>
      <img alt="Hashing Example" src="https://github.com/imaclone.x/Zencrypt/blob/main/zencrypthash.png" style="width: 100%; height: 100%;" />
    </center>
    <h3 align="center">Cipher:</h3>
    <center>
      <img alt="Cipher Example" src="https://github.com/imaclone.x/Zencrypt/blob/main/zencrypt.PNG" style="width: 100%; height: 100%;" />
    </center>
    <h3 align="center">Encrypting Parsed Files:</h3>
    <center>
      <img alt="Cipher Example" src="https://github.com/imaclone.x/Zencrypt/blob/main/encrypt.PNG" style="width: 100%; height: 50%;" />
    </center>
        <h3 align="center">PGP Encryption:</h3>
    <center>
      <img alt="Cipher Example" src="https://github.com/imaclone.x/Zencrypt/blob/main/pgpencryption.PNG" style="width: 100%; height: 50%;" />
    </center>
    </p>
    <hr><br>
    <h1 align="center" id="disclaimer"><bold>DISCLAIMER!</bold></h1>
    <p align="center">
      <strong>
        <=>
          <=>
            <=>
              <=>
                <=>
                  <=>
                    <=>
                      <=>
                        <=>
                          <=>
                            <=>
                              <=>
                                <=>
                                  <=>
                                    <=>
                                      <=>
                                        <=>
                                          <=>
                                            <=>
                                              <=>
                                                <=>
                                                  <=>
                                                    <=>
                                                      <=>
                                                        <=>
                                                          <=>
                                                            <!-- <=><=><=><=> -->
      </strong>
      </br>
      <!-- <p align="center"><strong><=><=><=></strong></br></p> -->
    <p align="center">
      <strong>
        <code>This script is provided for educational and demonstration purposes only. <br>Use it responsibly and please adhere to all applicable laws and regulations. </code>
      </strong>
      </br>
    </p>
    <!-- <strong>This script is provided for educational and demonstration purposes only. Use it responsibly and adhere to all applicable laws and regulations.</strong></br></p> -->
    <p align="center">
      <strong>
        <code>I am absolutely immune from any responsibility in regaurds to any damages or loss of data caused by the <br>use, abuse, or misuse of this software. </code>
      </strong>
      </br>
      <!-- <p align="center"><strong><=><=><=></strong></br></p> -->
    <p align="center">
      <strong>
        <=>
          <=>
            <=>
              <=>
                <=>
                  <=>
                    <=>
                      <=>
                        <=>
                          <=>
                            <=>
                              <=>
                                <=>
                                  <=>
                                    <=>
                                      <=>
                                        <=>
                                          <=>
                                            <=>
                                              <=>
                                                <=>
                                                  <=>
                                                    <=>
                                                      <=>
                                                        <=>
                                                          <=>
                                                            <!-- <=><=><=><=> -->
      </strong>
      </br>
    </p><hr>
    <h2 align="center" id="liscense">Liscense</h2>
    <p> This software is the property of the copyright holder and is protected by copyright laws. All rights are reserved. The copyright holder grants no implied or express license for the use, copying, modification, distribution, or reproduction of this software, in whole or in part, without the prior written permission of the copyright holder. </p>
    <p> Any unauthorized use, copying, modification, distribution, or reproduction of this software, in whole or in part, is strictly prohibited and constitutes a violation of copyright law. Such unauthorized use may result in civil and/or criminal penalties, including but not limited to legal action and monetary damages. </p>
    <p> To obtain permission for any use, copying, modification, distribution, or reproduction of this software, please contact the copyright holder at the following address: <code>imaclone.x@gmail.com</code>
    </p>
    </p>
    <br>
    <p align="center">
      <strong>
        <code>By using this software, you acknowledge that you have read and understood the terms of this license and agree to comply with all applicable copyright laws. <br>Failure to abide by the terms of this license may subject you to legal consequences. </code>
      </strong>
    </p>
  </body>
</html><hr>
<h2 align="center" id="contact">Contact</h2>
<p align="center">For any inquiries or suggestions, please contact me at <a href="mailto:imaclone.x@gmail.com">imaclone.x@gmail.com</a>.
</body>
</html>
