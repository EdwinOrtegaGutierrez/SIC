import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { RegistroComponent } from './components/registro/registro.component';
import { ContinueRegistroComponent } from './components/registro/continue-registro/continue-registro.component';

import {WebcamModule} from 'ngx-webcam';
import { NavbarComponent } from './components/navbar/navbar.component';
import { NavbarRComponent } from './components/registro/navbar-r/navbar-r.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegistroComponent,
    ContinueRegistroComponent,
    NavbarComponent,
    NavbarRComponent,
  ],
  imports: [
    WebcamModule,
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
