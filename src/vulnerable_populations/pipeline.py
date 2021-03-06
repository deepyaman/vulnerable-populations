# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Construction of the master pipeline.
"""

from enum import Enum, auto
from functools import reduce
from operator import add
from typing import Dict

from kedro.pipeline import Pipeline, pipeline

from vulnerable_populations.pipelines import data_engineering, preprocessing


class LowerName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


class Granularity(LowerName):
    COUNTY_LEVEL = auto()
    STATE_LEVEL = auto()


def create_pipelines(**kwargs) -> Dict[str, Pipeline]:
    """Create the project's pipeline.

    Args:
        kwargs: Ignore any additional arguments added in the future.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    pipelines = {}
    for granularity in Granularity:
        data_engineering_pipeline = pipeline(
            data_engineering.create_pipeline(),
            inputs={"raw_csbh_data": f"raw_csbh_{granularity.value}_data"},
            outputs={"int_csbh_data": f"int_csbh_{granularity.value}_data"},
            namespace=granularity,
        )
        pipelines[f"{granularity.value}.data_engineering"] = data_engineering_pipeline

        preprocessing_pipeline = pipeline(
            preprocessing.create_pipeline(),
            inputs={"int_csbh_data": f"int_csbh_{granularity.value}_data"},
            outputs={"mod_covid_19_master": f"mod_covid_19_{granularity.value}_master"},
            namespace=granularity,
        )
        pipelines[f"{granularity.value}.preprocessing"] = preprocessing_pipeline

    pipelines["__default__"] = reduce(add, pipelines.values())
    return pipelines
