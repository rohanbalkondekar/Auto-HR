import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonService } from 'src/app/common/common.service';

@Component({
  selector: 'app-post-new-job',
  templateUrl: './post-new-job.component.html',
  styleUrls: ['./post-new-job.component.scss']
})
export class PostNewJobComponent {

  jobTitle = '';
  aboutCompany = '';
  jobDescription: any;
  file: any;

  constructor(public commonService: CommonService, private router: Router){
  }

  closeSideNav(){
    this.commonService.close();
  }

  openFileChooser(){
    document.getElementById('file-chooser')?.click();
  }

  onFileChoose(event: any){
    this.file = event.target.files[0];
    console.log(this.file);

    if(this.file.type === 'text/plain'){
      let fileReader = new FileReader();
      fileReader.onload = (e) => {
        this.jobDescription = (fileReader?.result);
      }
      fileReader.readAsText(this.file);
    } else if(this.file.type === 'application/pdf'){

    } else if(this.file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'){

    }
  }


  openPreview(){
    this.closeSideNav();
    const data = {
      Job: this.jobTitle,
      About_Company: this.aboutCompany,
      Job_Description: this.jobDescription
    };
    localStorage.setItem('jobdata', JSON.stringify(data));
    this.router.navigate(['/home/preview']);
    this.jobTitle = '';
    this.aboutCompany = '';
  }


  validateForm(){
    if(this.jobTitle && this.aboutCompany && this.jobDescription){
      return true;
    }
    return false;
  }

  removeFile(){
    this.file = null;
  }
}
