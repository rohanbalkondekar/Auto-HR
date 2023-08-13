import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CommonService } from 'src/app/common/common.service';

@Component({
  selector: 'app-candidate-number',
  templateUrl: './candidate-number.component.html',
  styleUrls: ['./candidate-number.component.scss']
})
export class CandidateNumberComponent {

  candidateNumber = '';
  constructor(private _snackBar: MatSnackBar, private commonService: CommonService, public dialogRef: MatDialogRef<CandidateNumberComponent>){

  }

  sendMail(){
    this.commonService.sendMail(+this.candidateNumber).subscribe((response: any) => {
      if(response){
        this._snackBar.open('Email Send Successfully.', '',{
          horizontalPosition: 'end',
          verticalPosition: 'top',
          duration: 3000,
          panelClass: ['bgd-color'],
        });

        this.dialogRef.close();
      }
    })
    
  }
}
