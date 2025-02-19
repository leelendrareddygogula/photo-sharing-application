<h1>Photo Sharing Application</h1>
<p>This project allows users to upload images and view the previously uploaded images by any user. Furthermore, when an image is uploaded, a LLM API is called to generate a caption and description of the uploaded image. The caption and description were saved to a text file with the same name as the image in the bucket where images were uploaded. Later, when the image is requested by any user, the image is returned along with the caption and description. The requests are responded to by different instances deployed within the server to manage and coordinate the traffic to maintain low latency for each user. There are several endpoints associated with the project. Each endpoint has a different purpose. </p>
<h3>Technology Stacks</h3>
<table>
  <tr>
    <td>Front End</td>
    <td>HTML & CSS</td>
  </tr>
  <tr>
    <td>Backend</td>
    <td>Flask</td>
  </tr>
  <tr>
    <td>Database</td>
    <td>Google Storage</td>
  </tr>
  <tr>
    <td>Deployment</td>
    <td>Google Cloud Run</td>
  </tr>
</table>
<h3>Application End Points</h3>
<ol>
  <li>‘/’ - this is the landing page URI. This URI redirects the user to the page where the list of files will be displayed and allows the user to upload an image</li>
  <li>‘/upload’ - this URI is invoked when the user hits the submit button. This URI uploads the image to the selected cloud storage bucket and redirects the user to ‘/’</li>
  <li>‘/files/{image_name}’ - this is for the iteration of all the available images in the bucket on the home page. {image_name} is the name of the file to be fetched from the cloud storage</li>
  <li>‘/images/{image_name}’ - this URI displays the selected image in the HTML page</li>
</li>
</ol>
