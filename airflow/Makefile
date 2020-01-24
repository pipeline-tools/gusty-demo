
airflow_init:
	airflow initdb
	airflow variables -s datalake_user airflow
	airflow variables -s datalake_password airflow
	airflow variables -s datalake_host postgres
	airflow variables -s datalake_port 5432
	# set up views schema in database
	python3 setup_views.py

airflow_up:
	echo $(AIRFLOW_HOME)
	airflow scheduler &
	airflow webserver

airflow_down:
	 (pgrep -f airflow | xargs kill -9) &
	 sleep 1
	 jobs
	
airflow_clean:
	find . -name "*.log" -type f -delete
