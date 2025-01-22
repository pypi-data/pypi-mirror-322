import {
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  IRouter
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { IStatusBar } from '@jupyterlab/statusbar';
import createVersion from './widgets/createVersion';
import VersionListSidebarWidget from './widgets/version';
import DataSetListSidebarWidget from './widgets/dataset';
import UsageTimeWidget from './widgets/time';
import TitleWidget from './widgets/title';
import { getProjectDetail, getTaskDetail } from './api/project';
import { Notification } from '@jupyterlab/apputils';
import VariableInspectorPlugins from './widgets/variable/index';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { initializeSettings, saveApiConfig } from './utils/settings';

/**
 * 更新自动保存时间间隔
 */
async function updateAutosaveInterval(
  settingRegistry: ISettingRegistry,
  interval: number
) {
  const settingId = '@jupyterlab/docmanager-extension:plugin';
  try {
    const settings = await settingRegistry.load(settingId);
    await settings.set('autosaveInterval', interval);
  } catch (error) {
    console.error('Failed to update autosave interval:', error);
  }
}

/**
 * Activate the ln-notebook extension.
 */
async function activate(
  app: JupyterFrontEnd,
  palette: ICommandPalette,
  restorer: ILayoutRestorer | null,
  statusBar: IStatusBar,
  router: IRouter | undefined,
  settingRegistry: ISettingRegistry
): Promise<void> {
  console.log('Activating ln-jupyter-extra extension...');

  try {
    // 初始化设置管理器
    initializeSettings(settingRegistry);

    // 如果URL中有参数，保存到设置中
    const url = new URL(window.location.href);
    const type = url.searchParams.get('type');
    const auth = url.searchParams.get('auth');

    if (type || auth) {
      await saveApiConfig({
        baseUrl: type || undefined,
        authToken: auth || undefined
      });

      // // 清除URL中的参数
      // url.searchParams.delete('type');
      // url.searchParams.delete('auth');
      // window.history.replaceState({}, '', url.toString());
    }

    // 设置自动保存间隔
    await updateAutosaveInterval(settingRegistry, 30);

    // 处理路由
    if (router) {
      // 尝试获取路由信息
      const currentUrl = window.location.href;
      const pathSegments = currentUrl.split('/');
      const taskId = pathSegments[4];
      console.log('Task ID:', taskId);

      if (!taskId) {
        console.warn('No task ID found in URL');
        return;
      }

      const taskData = await getTaskDetail(taskId);
      const notebookProjectId = taskData.notebookProjectId;
      const clusterId = taskData.clusterId;
      console.log('Project ID:', notebookProjectId);

      const inputVolumeItem = taskData.jobStorageList.find(
        (item: any) => item.businessType === 0
      );
      const inputVolume = inputVolumeItem?.volumeTo || '';
      if (inputVolume) {
        try {
          const result = await app.serviceManager.contents.get(inputVolume);
          if (result?.content[0]?.path) {
            app.commands.execute('filebrowser:open-path', {
              path: result.content[0].path
            });
            console.log('Opened path:', result.content[0].path);
          }
        } catch (error) {
          console.error('Failed to access path:', error);
        }
      }

      if (!notebookProjectId) {
        throw new Error('Project ID not found');
      }

      // 初始化组件
      console.log('Initializing components...');
      const projectData = await getProjectDetail(notebookProjectId);

      const timeWidget = new UsageTimeWidget(taskId);
      timeWidget.install(app);

      const sidebarVersion = new VersionListSidebarWidget(
        app,
        notebookProjectId
      );
      sidebarVersion.install(app);

      const sidebarDataSet = new DataSetListSidebarWidget({
        clusterId,
        projectData
      });
      sidebarDataSet.install(app);

      const titleWidget = new TitleWidget({ projectData });
      titleWidget.install(app);

      const createVersionBtn = new createVersion(app, notebookProjectId);
      createVersionBtn.install(app);

      console.log('ln-jupyter-extra extension activated successfully!');
    } else {
      console.warn('Router not available');
    }
  } catch (error) {
    console.error('Error during activation:', error);
    Notification.error('插件激活失败: ' + (error as Error).message);
  }
}

const lnPlugin: JupyterFrontEndPlugin<void> = {
  id: 'ln-notebook:plugin',
  description: 'leinao extra jupyter plugin',
  autoStart: true,
  requires: [
    ICommandPalette,
    ILayoutRestorer,
    IStatusBar,
    IRouter,
    ISettingRegistry
  ],
  activate: activate
};

const plugins = [lnPlugin, ...VariableInspectorPlugins];
export default plugins;
