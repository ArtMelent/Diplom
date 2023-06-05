import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HighchartsChartModule } from 'highcharts-angular';
import { DefaultModule } from './layouts/default/default.module';
// import { CategoryListComponent } from './category-list/category-list.component';
import { CategoryComponent } from './category/category.component';
import { AutoLinkPipe } from './pipes/auto-link.pipe';
import { LanguageComponent } from './language/language.component';
import { HttpClientModule } from '@angular/common/http';
import { NotFoundComponent } from './not-found/not-found.component';
import { SharedModule } from './shared/shared.module';
import { TestSlidebarComponent } from './test-slidebar/test-slidebar.component';
import { CategoryDefaultService } from './services/category-default.service';
import { LanguageService } from './services/language.service';
import { BreadcrumbsComponent } from './breadcrumbs/breadcrumbs.component';
import { SubcategoryComponent } from './subcategory/subcategory.component';
import { CommonModule } from '@angular/common';
import { TagComponent } from './tag/tag.component';

@NgModule({
  declarations: [
    AppComponent,
    CategoryComponent,
    AutoLinkPipe,
    LanguageComponent,
    NotFoundComponent,
    TestSlidebarComponent,
    BreadcrumbsComponent,
    SubcategoryComponent,
    TagComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HighchartsChartModule,
    DefaultModule,
    HttpClientModule,
    SharedModule,
    CommonModule
    
  ],
  providers: [CategoryDefaultService, LanguageService],
  bootstrap: [AppComponent],
  exports: [
    TestSlidebarComponent,
    AutoLinkPipe
  ],
})
export class AppModule { }
