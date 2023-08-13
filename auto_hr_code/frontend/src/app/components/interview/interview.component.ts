import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonService } from 'src/app/common/common.service';

@Component({
  selector: 'app-interview',
  templateUrl: './interview.component.html',
  styleUrls: ['./interview.component.scss'],
})


export class InterviewComponent {
  question = '';
  questions_array: any[] = [];
  id = '';


  constructor(public comminService: CommonService, private route: ActivatedRoute, private router: Router){
    this.route.queryParams.subscribe((data) => {
      this.id = data['id'];
    })
  }
  ngOnInit() {
    window.addEventListener('beforeunload', (e) => {
      this.evaluateInterview();
    })
  }

  send() {
    const data = {
      User_Message: this.question
    }
    this.comminService.interview(this.id, data).subscribe((response: any) => {
      if(response) {
        this.questions_array = response.conversation;
        this.question = '';
        this.scrollBottom();

      }
    })
  }

  scrollBottom() {
    var objDiv = document.getElementById('chat-div') as HTMLDivElement;
    // objDiv.scrollTop = objDiv.scrollHeight;

    setTimeout(() => {
      objDiv.scrollTop = objDiv.scrollHeight - objDiv.clientHeight;
    }, 1000);
  }

  evaluateInterview(){
    this.comminService.isLoaderShow = true;
    this.comminService.evaluate_interview(this.id).subscribe((response: any) => {
      if(response){
        this.comminService.isLoaderShow = false;
       this.router.navigate(['/home/candidatejobs']);
      }
    })
  }

}
