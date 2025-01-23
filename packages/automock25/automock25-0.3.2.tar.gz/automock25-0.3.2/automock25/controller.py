from flask import render_template, jsonify
from status import get_config_params
import  logset
import  recordJob
# 设置日志
logger = logset.setup_logging
def init_routes(app):


    @app.route('/')
    def index():
        logger.info("Index page accessed")
        return "Flask App is running with job running in the background."

    @app.route('/status')
    def status():
        #logger.info("Status page accessed")
        config_params = get_config_params()
        job_status = "运行中" if recordJob.job_running else "停止"
        button_text = "停止" if recordJob.job_running else "运行"
        button_action = "/close_job" if recordJob.job_running else "/open_job"
        return render_template('status.html', config_params=config_params, job_status=job_status, button_text=button_text, button_action=button_action)

    @app.route('/close_job')
    def close_job():
        # 实现关闭 job 的逻辑
        if(recordJob.job_running):
            recordJob.jobPause()
            return jsonify({'res': '1','msg':'操作成功，已停止'})
        else:
            return jsonify({'res': '0','msg':'操作失败'})

    @app.route('/open_job')
    def open_job():
        # 实现打开 job 的逻辑
        if (recordJob.job_running):
            return jsonify({'res': '0', 'msg': '操作失败'})
        else:
            recordJob.jobRun()
            return jsonify({'res': '1', 'msg': '操作成功，已运行'})

