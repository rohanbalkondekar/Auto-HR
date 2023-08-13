import { Component, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { CommonService } from 'src/app/common/common.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  @ViewChild('sidenav') public sidenav: any;
  @ViewChild('applySidenav') public applySidenav: any

  isHrJobLoaded = true;

  constructor(public commonService: CommonService, private router: Router){
    this.isHrJobLoaded = this.router.url.includes('hrjobs');
  }
  
  ngAfterViewInit(){
    this.commonService.sidenav = this.sidenav;
    this.commonService.applySidenav = this.applySidenav;
  }

}
