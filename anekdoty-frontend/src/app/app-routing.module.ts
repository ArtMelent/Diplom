import { NgModule } from '@angular/core';
import { NavigationExtras, RouterModule, Routes, Router } from '@angular/router';
import { CategoryComponent } from './category/category.component';
import { LanguageComponent } from './language/language.component';
import { TagComponent } from './tag/tag.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { SubcategoryComponent } from './subcategory/subcategory.component';

const routes: Routes = [
  {
    path: 'not-found',
    component: NotFoundComponent
  },
  {
    path: ':langUrl',
    children: [
      {
        path: '',
        component: LanguageComponent
      },
      {
        path: ':category_url',
        children: [
          {
            path: '',
            component: CategoryComponent
          },
          {
            path: ':subcategory_url',
            children: [
              {
                path: '',
                component: SubcategoryComponent
              },
              {
                path: ':tag_url',
                children: [
                  {
                    path: '',
                    component: TagComponent
                  },
                  {
                    path: ':subtag_url',
                    component: TagComponent
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  { path: '**', redirectTo: '/not-found', pathMatch: 'full' },
];



@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }

