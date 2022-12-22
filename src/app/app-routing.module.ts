import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { ContinueRegistroComponent } from './components/registro/continue-registro/continue-registro.component';
import { RegistroComponent } from './components/registro/registro.component';

const routes: Routes = [
  {
    path:"",
    component:LoginComponent
  },
  {
    path:"registro",
    component:RegistroComponent
  },
  {
    path:"scaner",
    component:ContinueRegistroComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
