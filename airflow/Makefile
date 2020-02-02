
airflow_init:
	airflow upgradedb
	airflow variables -s EZ_AF_USER ${EZ_AF_USER}
	airflow connections -a --conn_id postgres_datalake --conn_uri postgresql://${EZ_AF_USER}:${EZ_AF_PASSWORD}@postgres:5432/datalake
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
