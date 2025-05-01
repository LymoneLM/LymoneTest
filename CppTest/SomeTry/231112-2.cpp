int n;
char dat[51][50],temp[51];
for (int i = 0; i < n-1; i++) {
		int min = i;
		for (int j = i; j < n; j++) {
			if (strcmp(dat+min,dat+j)>0) {
				min = j;
			}
		}
		if (min != i) {
            strcpy(temp,dat+min);
			strcpy(dat+min,dat+i);
            strcpy(dat+i,temp);
		}
	}

