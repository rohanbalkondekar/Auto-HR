import { Component } from '@angular/core';
import { CommonService } from 'src/app/common/common.service';

@Component({
  selector: 'app-job-details',
  templateUrl: './job-details.component.html',
  styleUrls: ['./job-details.component.scss']
})
export class JobDetailsComponent {

  constructor(public commonService: CommonService){}
  openApplySideNav(){
    this.commonService.openApplySideNav();
  }
}
