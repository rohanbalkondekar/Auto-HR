import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { CommonService } from 'src/app/common/common.service';

@Component({
  selector: 'app-view-interview-applicants',
  templateUrl: './view-interview-applicants.component.html',
  styleUrls: ['./view-interview-applicants.component.scss']
})
export class ViewInterviewApplicantsComponent {

  candidateList:any[] = [];
  constructor(private commonSerivce: CommonService, @Inject(MAT_DIALOG_DATA) public data: any){
  }

  ngOnInit(){
    this.getCandidateList();
  }

  getCandidateList(){
    this.commonSerivce.getInterviewByJobId(this.data.Job_ID).subscribe((response: any) => {
      if(response){
        const candidateDataList = response as Array<any>;
        candidateDataList.forEach(item => {
          const data = {
            name: item['Applicant_Details'] ? item['Applicant_Details']['Name'] : 'Not Found',
            status: item['interview_result'] ? item['interview_result']['proceed_to_next_round'] ? 'Passed' : 'Rejected' : 'Rejected',
            reason: item['interview_result'] ? item['interview_result']['reason'] : ''
          };
          this.candidateList.push(data);
        })
      }
    })
  }
}
