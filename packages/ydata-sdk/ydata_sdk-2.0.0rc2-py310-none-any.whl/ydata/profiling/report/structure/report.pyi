from ydata.profiling.model import BaseDescription
from ydata_profiling.config import Settings as Settings
from ydata_profiling.report.presentation.core.renderable import Renderable as Renderable
from ydata_profiling.report.presentation.core.root import Root

def get_report_structure(config: Settings, summary: BaseDescription) -> Root: ...
def render_variables_section(config: Settings, dataframe_summary: BaseDescription) -> list: ...
