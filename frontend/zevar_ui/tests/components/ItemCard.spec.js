import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import ItemCard from '../../src/components/ItemCard.vue'

const item = {
	item_code: 'ITEM-001',
	item_name: 'Diamond Ring',
	price: 1200,
	stock_qty: 3,
	metal: 'Yellow Gold',
	purity: '18K',
}

describe('ItemCard', () => {
	it('emits quick-add once when the add button is clicked', async () => {
		const wrapper = mount(ItemCard, {
			props: { item },
		})

		await wrapper.find('button[title="Add to Cart"]').trigger('click')

		expect(wrapper.emitted('quick-add')).toHaveLength(1)
		expect(wrapper.emitted('quick-add')[0]).toEqual([item])
		expect(wrapper.emitted('open-details')).toBeUndefined()
	})

	it('opens item details when the card body is clicked', async () => {
		const wrapper = mount(ItemCard, {
			props: { item },
		})

		await wrapper.trigger('click')

		expect(wrapper.emitted('open-details')).toHaveLength(1)
		expect(wrapper.emitted('open-details')[0]).toEqual([item.item_code])
	})
})
