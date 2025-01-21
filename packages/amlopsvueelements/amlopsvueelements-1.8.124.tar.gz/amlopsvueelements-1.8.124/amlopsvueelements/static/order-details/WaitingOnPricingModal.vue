<template>
  <div v-if="props.isOpen" class="order-modal waiting-pricing-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes is-modal>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-lg font-semibold text-base-800">
                  Mark as Waiting on Supplier Pricing
                </div>
                <button @click.stop="emit('modal-close')">
                  <img
                    width="12"
                    height="12"
                    src="../../assets/icons/cross.svg"
                    alt="delete"
                    class="close"
                  />
                </button>
              </div>
            </template>
            <template #content>
              <div class="form-body-wrapper">
                <div class="flex mb-[0.75rem]">
                  <div class="w-3/12 flex items-center text-subtitle">Uplift Date</div>
                  <div class="w-6/12 flex items-center text-base-900 font-medium">
                    {{ order?.fulfilment_datetime.slice(0, 10) }}
                  </div>
                </div>
                <div
                  v-for="(reminder, reminderIndex) in reminders"
                  :key="reminderIndex"
                  class="flex mb-[0.75rem] justify-end"
                >
                  <div
                    v-show="reminderIndex === 0"
                    class="w-3/12 flex items-center text-subtitle text-sm"
                  >
                    Reminder
                  </div>
                  <div class="w-5/12">
                    <InputField
                      :model-value="reminders[reminderIndex]"
                      type="number"
                      class="w-full mb-0"
                      :input-class="$style['days-input']"
                      placeholder=""
                      @update:model-value="($e) => onChangeDays($e, reminderIndex)"
                    >
                      <template #suffix>
                        <div class="input-suffix text-nowrap">day(s) before</div>
                      </template>
                    </InputField>
                  </div>
                  <div class="w-3/12 flex items-center justify-center text-subtitle">
                    {{ subtractDaysFromDate(new Date(order!.fulfilment_datetime), reminder) }}
                  </div>
                  <div class="flex shrink-0 w-1/12">
                    <img
                      v-if="reminders?.length > 1"
                      width="20"
                      height="20"
                      src="../../assets/icons/cross-red.svg"
                      alt="delete"
                      class="cursor-pointer"
                      @click="deleteReminder(reminderIndex)"
                    />
                  </div>
                </div>
                <div
                  v-show="reminders.length < 3"
                  class="handling-step-add-service flex cursor-pointer py-[0.75rem] gap-2 w-fit ml-[25%] text-subtitle"
                  @click="addReminder"
                >
                  <img src="../../assets/icons/plus.svg" alt="add" />
                  Add Reminder
                </div>
              </div>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <Loading v-if="isLoading" class="mr-4" />
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button
            class="modal-button submit"
            :disabled="!reminders.length || isLoading"
            @click.stop="onValidate()"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, type Ref, ref } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { useOrderStore } from '@/stores/useOrderStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import { useMutationWaitingOnSupplierPricing } from '@/services/mutations';
import { subtractDaysFromDate } from '@/helpers/order';
import { notify } from '@/helpers/toast';
import InputField from '../forms/fields/InputField.vue';
import Loading from '../forms/Loading.vue';

const props = defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['modal-close', 'modal-submit']);

const queryClient = useQueryClient();
const orderStore = useOrderStore();
const target = ref(null);

const order = computed(() => orderStore.order);
const orderId = computed(() => orderStore.orderId);

const reminders: Ref<number[]> = ref([1]);

const { mutate: waitingOnSupplierPricingMutation, isPending: isLoading } =
  useMutationWaitingOnSupplierPricing();

const addReminder = () => {
  const lastReminder = reminders.value[reminders.value.length - 1];
  reminders.value.push(lastReminder ? lastReminder + 1 : 1);
};

const onChangeDays = (days: string, index: number) => {
  reminders.value[index] = parseInt(days);
};

const deleteReminder = (index: number) => {
  reminders.value.splice(index, 1);
};

const validate = () => {
  let isValid = true;
  reminders.value.forEach((el) => {
    if (
      el === undefined ||
      new Date(subtractDaysFromDate(new Date(order.value!.fulfilment_datetime), el!)) < new Date()
    )
      isValid = false;
  });
  return isValid;
};

const onValidate = async () => {
  const isValid = validate();

  if (!isValid) {
    return notify('Error while submitting, reminder date should not exceed present date!', 'error');
  } else {
    const payload = reminders.value.map((reminder) => ({
      days_before: reminder!
    }));

    await waitingOnSupplierPricingMutation(
      {
        orderId: orderId.value,
        payload
      },
      {
        onSuccess: () => {
          notify('Marked as waiting on supplier pricing', 'success');
          queryClient.invalidateQueries({ queryKey: ['orderStatus', orderId] });
          emit('modal-close');
          emit('modal-submit');
        }
      }
    );
  }
};
</script>

<style module lang="scss">
.waiting-pricing-modal {
  .input-suffix {
    width: -webkit-fill-available;
  }

  .order-modal-footer {
    align-items: center;
    flex: 0 0 72px;
    min-height: 72px;

    .modal-button {
      max-height: 44px;
    }
  }
}

.days-input {
  font-size: 1rem !important;
  font-weight: 400 !important;
}
</style>
