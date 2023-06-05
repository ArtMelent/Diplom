import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Router, UrlSegment } from '@angular/router';
import { filter } from 'rxjs/operators';

interface Breadcrumb {
  label: string;
  url: string;
}

@Component({
  selector: 'app-breadcrumbs',
  templateUrl: './breadcrumbs.component.html',
  styleUrls: ['./breadcrumbs.component.scss']
})
export class BreadcrumbsComponent implements OnInit {
  breadcrumbs: Breadcrumb[] = [];

  constructor(private router: Router, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        this.generateBreadcrumbs(this.route.root);
      });
  }

  generateBreadcrumbs(route: ActivatedRoute, url: string = '', breadcrumbs: Breadcrumb[] = []): void {
    const routeData = route.snapshot.data;

    if (routeData && routeData['breadcrumb']) {
      const breadcrumb: Breadcrumb = {
        label: routeData['breadcrumb'],
        url: url
      };
      breadcrumbs.push(breadcrumb);
    }

    const firstChild = route.firstChild;
    if (firstChild) {
      firstChild.url.subscribe((segments: UrlSegment[]) => {
        const path = segments.map(segment => segment.path).join('/');
        this.generateBreadcrumbs(firstChild, `${url}/${path}`, breadcrumbs);
      });
    }

    this.breadcrumbs = breadcrumbs;
  }
}
